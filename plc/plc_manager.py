import threading
import time
import snap7
from plc_read.plcReadLen import read_len
from plc_read.plcReadTrig import read_trigger_def
from plc_read.resetTrig import res_trigger
from config import plc_ip, rack,slot

class PlcManager:
    def __init__(self):
        self.ip = plc_ip  # Берём IP из config
        self.rack = rack  # Берём rack из config
        self.slot = slot  # Берём slot из config
        self.plc = snap7.client.Client()
        self.connected = False
        self.running = False
        self.lock = threading.Lock()

        # Актуальные данные
        self.length = 0.0
        self.trigger = False

    def connect(self):
        """Подключается к ПЛК."""
        try:
            self.plc.connect(self.ip, self.rack, self.slot)
            self.connected = True
            print(f"✅ Подключено к ПЛК ({self.ip})")
        except Exception as e:
            print(f"❌ Ошибка подключения к ПЛК: {e}")

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
        with self.lock:
            self.length = read_len(self.plc)
            self.trigger = read_trigger_def(self.plc)

    def reset_trigger(self):
        """Сбрасывает триггер."""
        with self.lock:
            res_trigger(self.plc)

    def start(self):
        """Запускает цикл чтения данных с ПЛК."""
        self.running = True
        self.connect()

        try:
            while self.running:
                self.read_data()
                time.sleep(0.2)  # Частота опроса ПЛК (5 Гц)
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