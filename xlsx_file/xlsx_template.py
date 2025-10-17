import os
import shutil
import logging

def replace_xlsx_with_template(target_path, template_path):
    """
    Заменяет целевой XLSX-файл шаблоном из другой папки.

    :param target_path: Путь к целевому файлу (который нужно заменить).
    :param template_path: Путь к файлу-шаблону (исходный файл для подмены).
    """
    try:
        # 1. Проверяем, существует ли целевой файл
        if os.path.exists(target_path):
            print(f"ℹ️ Целевой файл найден: {target_path}")
            logging.info(f"ℹ️ Целевой файл найден: {target_path}")

            # 2. Пытаемся закрыть файл, если он открыт
            try:
                # Для Windows: проверяем, открыт ли файл
                if os.name == 'nt':  # Windows
                    os.system(f'taskkill /IM "EXCEL.EXE" /F')  # Закрываем Excel, если файл открыт в нем
                else:
                    print("⚠️ На других ОС закрытие файла не реализовано.")
            except Exception as e:
                print(f"⚠️ Не удалось закрыть файл: {e}")

            # 3. Удаляем целевой файл
            os.remove(target_path)
            print(f"🗑️ Целевой файл удален: {target_path}")

        # 4. Копируем шаблон на место целевого файла
        shutil.copy(template_path, target_path)
        print(f"✅ Шаблон скопирован: {template_path} -> {target_path}")

    except Exception as e:
        print(f"❌ Ошибка при замене файла: {e}")
        logging.error(f'ошибка по замене файла')