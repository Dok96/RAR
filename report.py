import threading
import time
import logging
from stopScript.stp import input_listener
from plc.plc_manager import PlcManager  # Новый модуль для управления ПЛК


from Lump.Lump_main import main_lump_func


# Настройка логирования
logging.basicConfig(
    filename="script_log.txt",       # Имя файла для логов
    filemode="a",                    # Режим записи: 'a' (append) — добавление в конец файла
    format="%(asctime)s - %(levelname)s - %(message)s",  # Формат логов
    level=logging.INFO               # Уровень логирования: INFO и выше
)

# Создаём объект Event для управления состоянием
stop_event = threading.Event()



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

    # запускаем поток для обработки данных и формирования xlsx для lump
    # Запускаем поток для обработки данных и формирования xlsx для Lump
    lump_thread = threading.Thread(
        target=main_lump_func,
        args=(
            stop_event,
            length,
            external_vars["basy_gen_report"],
            external_vars["gen_report_complate"]
        ),
        daemon=True
    )
    lump_thread.start()

    # Запускаем основную задачу
    try:
        main_task(plc_manager)
    except KeyboardInterrupt:
        print("\n🛑 Принудительная остановка (Ctrl+C).")
        logging.warning("Принудительная остановка (Ctrl+C).")
    finally:
        stop_event.set()  # Устанавливаем флаг завершения
        plc_manager.stop()  # Останавливаем поток чтения с ПЛК
        print("Скрипт завершён.")
        logging.info("скрипт завершён")