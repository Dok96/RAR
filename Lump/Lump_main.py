# main Lump обработка всего сценария для датчика Lump

from Lump.xlsx_lump_report import save_to_xlsx # функция создания отчёта
from Lump.lump_read import poll_sensor  # сброс активного дефекта
from xlsx_file.xlsx_template import replace_xlsx_with_template # Функция замена текущего отчёта на чистый шаблон


from config import dist_lump_report, dist_template_Lump_report #
from Lump.global_Lump import fault_active_val # глобальная переменная


def main_lump_func(stop_event,lenght_current, basy_gen_report,gen_report_complate):
    global fault_active_val
    while not stop_event.is_set():  # Работаем, пока не установлен флаг завершения
        try:
            # вызов функции для чтения данных с Lump
            result_lump = poll_sensor(1)
            fault_count = result_lump.get("fault_count")
            fault_num = result_lump.get("fault_num")
            fault_active_val = result_lump.get("fault_active")
            fault_height_mm = result_lump.get("fault_height_mm")
            fault_length_mm = result_lump.get("fault_length_mm")
            meter_counter_m = result_lump.get("meter_counter_m")

            # в случае обнаружения ошибки делаем запись в xlsx если нет basy_gen_report (формирование основного отчёта)
            if fault_active_val and not basy_gen_report :
                result_xlsx = save_to_xlsx(fault_active_val, fault_num, lenght_current, fault_count, dist_lump_report)
                fault_active_val

            # сбрасываем после того как главный отчёт был сформирован
            if gen_report_complate and not basy_gen_report :
                replace_xlsx_with_template(dist_lump_report, dist_template_Lump_report)

            return fault_active_val

        except ValueError:
            print(f' ошибка выполнения main lump')

