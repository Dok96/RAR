import threading
import time
from stopScript.stp import input_listener
from plc.plc_manager import PlcManager  # Новый модуль для управления ПЛК
from config import plc_ip,slot,rack, db_number,offset_len,offset_trigger

# Создаём объект Event для управления состоянием
stop_event = threading.Event()

def main_task(plc_manager):
    """
    Основной поток: выполняет задачи, пока stop_event не установлен.
    """
    print(f'plc_ip:{plc_ip}, slot:{slot}, rack {rack},'
          f'\n db № {db_number} : \n длина dbd{offset_len} ,\n триггер: dbx4.0,\n линия в работе: dbx4.1,'
          f'\n запрос в ручном режиме dbx4.2')

    # получаем данные из скрипта plc_manager
    while not stop_event.is_set():  # Проверяем флаг
        # Получаем актуальные данные с ПЛК
        length = plc_manager.get_length()
        trigger = plc_manager.get_trigger()  # триггер формирования протокола
        lineRun = plc_manager.get_line_run()  # триггер линия в работе
        manReqProtocol = plc_manager.get_man_req_protocol() # триггер формирование протокола в ручном режиме


        #print(f"Длина : {length}, триггер : {trigger}")
        #time.sleep(3)

        if trigger == True and not p1:
            print(f"Длина : {length}, триггер : {trigger}, Run: : {lineRun}, manReq : {manReqProtocol}")

            #сброс триггера
            time.sleep(3)
            plc_manager.reset_trigger()
            plc_manager.lump_send_fault_plc()
            plc_manager.spark_send_fault_plc()


        p1=trigger


if __name__ == "__main__":
    print("Запуск скрипта... Для остановки введите 'Y'.")

    # Создаём объект для работы с ПЛК
    plc_manager = PlcManager()

    # Запускаем поток для чтения данных с ПЛК
    plc_thread = threading.Thread(target=plc_manager.start, daemon=True)
    plc_thread.start()

    # Запускаем поток для ввода
    input_thread = threading.Thread(target=input_listener, args=(stop_event,), daemon=True)
    input_thread.start()

    # Запускаем основную задачу
    try:
        main_task(plc_manager)
    except KeyboardInterrupt:
        print("\n🛑 Принудительная остановка (Ctrl+C).")
    finally:
        stop_event.set()  # Устанавливаем флаг завершения
        plc_manager.stop()  # Останавливаем поток чтения с ПЛК

        print("Скрипт завершён.")