import os

def load_config(file_path):
    """
    Загружает конфигурацию из текстового файла.
    Возвращает словарь с параметрами.
    """
    config = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Пропускаем комментарии и пустые строки
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # Разделяем строку на ключ и значение
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Преобразуем числовые значения
                    if value.isdigit():
                        value = int(value)
                    elif value.replace('.', '', 1).isdigit():
                        value = float(value)

                        # Если значение является путем, заменяем обратные слеши на прямые
                    if key in ["source_template_report", "", "",
                                "", "", "", ""]:
                        value = value.replace("\\", "/")

                    config[key] = value
    except FileNotFoundError:
        print(f"Файл конфигурации не найден: {file_path}")
    except Exception as e:
        print(f"Ошибка при чтении конфигурации: {e}")

    return config

# Путь к файлу конфигурации
CONFIG_FILE = "config.txt"

# Загрузка конфигурации
config = load_config(CONFIG_FILE)

running = True # общая переменная


# # Доступ к параметрам через глобальные переменные
# source = config.get("source")
# destination = config.get("destination")
# interval = config.get("interval", 1)  # Значение по умолчанию
# m_retries = config.get("m_retries", 200)
#
# source_template_Xl = config.get("source_template_Xl")


#==Report==
source_template_report = config.get("template_report")

dist_report_pdf= config.get("dist_report_pdf") # путь для pdf
dist_report_xlsx = config.get("dist_report_xlsx") # путь для xlsx


#==PLC==
#==connect
plc_ip = config.get("plc_ip")
rack = config.get("rack")
slot = config.get("slot")
retry_delay = config.get("retry_delay", 5)

#==message (длина и тригер формирования сообщения)
#  номер дата блока
db_number = config.get("db_number")
# размещение тега триггера
offset_len = config.get("offset_len")
# размещение тега триггера
offset_trigger = config.get("offset_trigger")

# время опроса тегов
time_tag = config.get("time_tag", 0.2)

#print(f"{db_number} ; {offset_len}, {offset_trigger}")



