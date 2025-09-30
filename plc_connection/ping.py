import os
from  config import   plc_ip


def ping_plc():
    """
    Проверяет доступность PLC с помощью ping.
    Возвращает True, если ping успешен, иначе False.
    """
    try:
        # Для Windows
        response = os.system(f"ping -n 1 -w 1000 {plc_ip} >nul")
        # Для Linux/macOS (если вы используете эти ОС, раскомментируйте следующую строку)
        # response = os.system(f"ping -c 1 -W 1 {ip_address} > /dev/null 2>&1")
        return response == 0
    except Exception as e:
        print(f"Ошибка при проверке ping: {e}")
        return False
