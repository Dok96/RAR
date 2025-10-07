import threading
import time
import snap7
from plc_read.plcReadLen import read_len
from plc_read.plcReadTrig import read_trigger_def
from plc_read.resetTrig import res_trigger
from plc_read.plc_alarm_Lump import lump_send_fault_plc
from plc_read.plc_alarm_Spark import spark_send_fault_plc

from config import plc_ip, rack,slot, time_tag, MAX_retry_delay,retry_delay

class PlcManager:
    def __init__(self):
        self.ip = plc_ip  # Берём IP из config
        self.rack = rack  # Берём rack из config
        self.slot = slot  # Берём slot из config
        self.MAX_retry_delay=MAX_retry_delay
        self.retry_delay = retry_delay
        self.plc = snap7.client.Client()
        self.connected = False
        self.running = False
        self.lock = threading.Lock()

        # Актуальные данные
        self.length = 0.0
        self.trigger = False
        self.lineRun=False
        self.manReqProtocol=False

    def connect(self):
        """Подключается к ПЛК."""
        """Подключается к ПЛК с повторными попытками каждые 5 секунд."""
        while self.running:  # Пока поток запущен
            try:
                self.plc = snap7.client.Client()  # Создаём новый объект Client
                self.plc.connect(self.ip, self.rack, self.slot)
                self.connected = True
                print(f"✅ Подключено к ПЛК ({self.ip})")
                self.retry_delay = retry_delay  # Сбрасываем задержку после успешного подключения
                break # Выходим из цикла при успешном подключении
            except Exception as e:
                print(f"❌ Ошибка подключения к ПЛК: {e}. \n Повторная попытка через {self.retry_delay} секунд...")
                time.sleep( self.retry_delay)  # Ждём 5 секунд перед следующей попыткой
                self.retry_delay= min(self.retry_delay+10,self.MAX_retry_delay)


    def disconnect(self):
        """Отключается от ПЛК."""
        try:
            if self.connected:
                self.plc.disconnect()
                print("🔌 Соединение с ПЛК закрыто")
        except Exception as e:
            print(f"⚠️ Ошибка при отключении: {e}")

    def read_data(self):
        """Читает длину провода и статус триггера."""
        try:
            #проверяем соединение
            if not self.plc.get_connected():
                print("⚠️ Соединение с плк потеряно ")
                self.connected=False
                return

            with self.lock:
                self.length = read_len(self.plc)
                trigger_report, lineRun, manReqProtocol  = read_trigger_def(self.plc)  # Получаем три значения
                self.trigger =trigger_report
                self.lineRun = lineRun
                self.manReqProtocol = manReqProtocol


        except Exception as e:
            print(f"Error : {e}")
            self.connected = False  # Отмечаем, что соединение разорвано

    def reset_trigger(self):
        """Сбрасывает триггер."""
        with self.lock:
            res_trigger(self.plc)

    # активировать тэг ошибки  по люмпу
    def lump_send_fault_plc(self):

        with self.lock:
            lump_send_fault_plc(self.plc)

    # активировать тэг ошибки  по spark
    def spark_send_fault_plc(self):

        with self.lock:
           spark_send_fault_plc(self.plc)
################################################################3
    def start(self):
        """Запускает цикл чтения данных с ПЛК."""
        self.running = True
        self.connect()

        try:
            while self.running:
                if not self.connected:
                    print("⚠️ Соединение с ПЛК потеряно. Попытка переподключения...")
                    self.connect()  # Переподключаемся, если соединение потеряно
                else:
                    self.read_data()
                    time.sleep(time_tag)  # Частота опроса ПЛК (5 Гц)
        except Exception as e:
            print(f"❌ Ошибка в потоке чтения ПЛК: {e}")
        finally:
            self.disconnect()

    def stop(self):
        """Останавливает поток чтения данных с ПЛК."""
        self.running = False

    def get_length(self):
        """Возвращает текущую длину провода."""
        with self.lock:
            return self.length

    def get_trigger(self):
        """Возвращает текущий статус триггера."""
        with self.lock:
            return self.trigger

    def get_line_run(self):
        """Возвращает текущий статус 'линия в работе'."""
        with self.lock:
            return self.lineRun

    def get_man_req_protocol(self):
        """Возвращает текущий статус 'формирование протокола в ручном режиме'."""
        with self.lock:
            return self.manReqProtocol


