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
          f'\n db № {db_number} ,длина {offset_len} , треггер {offset_trigger}')

    # получаем данные из скрипта plc_manager
    while not stop_event.is_set():  # Проверяем флаг
        # Получаем актуальные данные с ПЛК
        length = plc_manager.get_length()
        trigger = plc_manager.get_trigger()

        print(f"Длина : {length}, триггер : {trigger}")
        time.sleep(3)

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