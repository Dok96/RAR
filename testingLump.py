from Lump.xlsx_lump_report import save_to_xlsx
from Lump.lump_read import reset_fault_active
from config import dist_lump_report, dist_template_Lump_report
from Lump.global_Lump import fault_active_val # глобальная переменная
from xlsx_file.xlsx_template import replace_xlsx_with_template

while True:

    try:
        global fault_active_val
        complate_xlsx = False
        # Ввод числа
        fault_type = int(input("Введите целое число: "))

        # Ввод да/нет
        answer = input("Введите 'да' или 'нет': ").lower().strip()

        if answer in ['да', 'д', 'yes', 'y', 'true', '1']:
            fault_active_val = True
        elif answer in ['нет', 'н', 'no', 'n', 'false', '0']:
            fault_active_val = False
        else:
            print("Неверный ввод! Попробуйте снова.")
            continue

            # Ввод да/нет
        answer_2 = input("Введите 'да' или 'нет': ").lower().strip()

        if answer_2 in ['да', 'д', 'yes', 'y', 'true', '1']:
            change_xlsx = True
        elif answer_2 in ['нет', 'н', 'no', 'n', 'false', '0']:
            change_xlsx = False


        # Обработка корректных данных
        print(f"Логическое значение: {fault_active_val}")
        print(f"Тип данных: {type(fault_active_val)}")

        complate_xlsx =save_to_xlsx(fault_active_val, fault_type, 100, 3, dist_lump_report)

        if fault_active_val and complate_xlsx:
            fault_active_val= reset_fault_active()
            complate_xlsx = False


        print(f"Скрипт сохранения xlsx выполнен")
        print(f"fault_active: {fault_active_val}")

        if change_xlsx :
           replace_xlsx_with_template(dist_lump_report, dist_template_Lump_report)
           print(f"шаблон обнавлён")

        else:
           continue

    except ValueError:
        print("Ошибка! Введите корректное целое число.")
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем.")
        break