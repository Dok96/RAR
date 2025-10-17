import serial
import logging

# Настройка логирования
logging.basicConfig(
    filename="sensor_log.txt",  # Имя файла для логов
    filemode="a",               # Режим записи: 'a' (append)
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO         # Уровень логирования: INFO и выше
)

# Глобальные переменные
fault_count_rec = 0  # Предыдущее значение счетчика дефектов
fault_active = False  # Флаг активности дефекта

def poll_sensor(port, baudrate=115200, timeout=1):
    """
    Опрашивает датчик SIKORA LUMP через интерфейс RS-232 и возвращает данные о дефектах и ошибках.

    :param port: Порт для подключения к датчику (например, "COM1").
    :param baudrate: Скорость передачи данных (по умолчанию 115200).
    :param timeout: Таймаут ожидания ответа (в секундах).
    :return: Словарь с данными о дефектах и флагами ошибок.
    """
    global fault_count_rec, fault_active  # Используем глобальные переменные

    try:
        # Запрос Actual Fault (HEX): 02 33 31 30 03 31
        request = bytes([0x02, 0x33, 0x31, 0x30, 0x03, 0x31])

        # Открываем последовательный порт
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            logging.info(f"Открыт порт {port} со скоростью {baudrate}.")

            # Отправляем запрос
            ser.write(request)
            logging.info("Запрос отправлен.")

            # Читаем ответ (ожидаем 22 байта)
            response = ser.read(22)
            if not response:
                logging.error("Таймаут при чтении ответа.")
                return {"error": "Timeout error"}

            # Логируем полученный ответ
            logging.info(f"Получен ответ: {response.hex()}")

            # Проверка CRC
            crc_received = response[-1]
            crc_calculated = calculate_crc(response[:-1])
            if crc_received != crc_calculated:
                logging.error(f"CRC не совпадает: получен {crc_received}, рассчитан {crc_calculated}.")
                return {"error": "CRC mismatch"}

            # Обработка данных
            fault_count = int(response[4:8].decode(), 16)
            fault_num = int(response[8:9].decode())
            fault_height = int(response[9:12].decode()) / 100
            fault_length = int(response[12:15].decode()) / 10
            meter_counter = int(response[15:20].decode())

            # Расшифровка типа дефекта

            if fault_count > fault_count_rec:
                fault_active = True  # Активируем флаг ошибки

            elif fault_count == fault_count_rec:
                fault_active = False  # Сохраняем текущее состояние флага


            # Обновляем значение предыдущего счетчика дефектов
            fault_count_rec = fault_count

            # Возвращаем результат
            return {
                "fault_count": fault_count,
                "fault_num": fault_num,
                "fault_active": fault_active,
                "fault_height_mm": fault_height,
                "fault_length_mm": fault_length,
                "meter_counter_m": meter_counter,
                "error": None
            }

    except Exception as e:
        logging.error(f"Ошибка при опросе датчика: {e}")
        return {"error": str(e)}


def calculate_crc(data):
    """
    Рассчитывает контрольную сумму (CRC) для данных.

    :param data: Байтовый массив данных.
    :return: Рассчитанная контрольная сумма.
    """
    crc = 0
    for byte in data:
        crc ^= byte
    if crc < 0x20:
        crc += 0x20
    return crc


#Для теста. Пример использования
if __name__ == "__main__":
    port = "COM1"  # Порт для подключения к датчику
    result = poll_sensor(port)

    if result["error"]:
        print(f"Ошибка: {result['error']}")
    else:
        print(f"Данные о дефектах:")
        print(f"  Количество дефектов: {result['fault_count']}")
        print(f"  Тип дефекта: {result['fault_type']}")
        print(f"  Высота дефекта: {result['fault_height_mm']} мм")
        print(f"  Длина дефекта: {result['fault_length_mm']} мм")
        print(f"  Метраж: {result['meter_counter_m']} м")
        print(f"  Активность дефекта: {'Да' if result['fault_active'] else 'Нет'}")