import time
from config import retry_delay

def connect_to_plc(plc_obj, ip_address, rack_num, slot_num):
    """
    Подключение к ПЛК с повторными попытками.
    Перед подключением всегда выполняется отключение (disconnect).
    """
    while True:
        try:
            # Отключаемся, если соединение существует
            if plc_obj.get_connected():
                try:
                    plc_obj.disconnect()
                    print("Соединение с ПЛК закрыто.")
                except Exception as e:
                    print(f"Ошибка при отключении: {e}")

            # Попытка подключения
            print("Попытка подключения к ПЛК...")
            plc_obj.connect(ip_address, rack_num, slot_num)
            if plc_obj.get_connected():
                print("Подключение к ПЛК успешно установлено.")
                return True

        except Exception as e:
            print(f"Ошибка подключения: {e}")

        print(f"Повторная попытка подключения через {retry_delay} секунд...")
        time.sleep(retry_delay)