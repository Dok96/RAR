from config import (plc_ip,slot,rack, db_number,offset_len,offset_trigger,
                    template_report, blank_report)
from xlsx_file.xlsx_template import replace_xlsx_with_template

def main_task(stop_event,plc_manager):
    """
    Основной поток: выполняет задачи, пока stop_event не установлен.
    """
    logging.info("Запуск основного потока.")
    print(f'plc_ip:{plc_ip}, slot:{slot}, rack {rack},'
          f'\n db № {db_number} : \n длина dbd{offset_len} ,\n триггер: dbx4.0,\n линия в работе: dbx4.1,'
          f'\n запрос в ручном режиме dbx4.2')

    p1 = None  # Переменная для хранения предыдущего состояния триггера

    # получаем данные из скрипта plc_manager
    while not stop_event.is_set():  # Проверяем флаг
        try:
            # Получаем актуальные данные с ПЛК
            length = plc_manager.get_length()
            trigger = plc_manager.get_trigger()  # триггер формирования протокола
            lineRun = plc_manager.get_line_run()  # триггер линия в работе
            manReqProtocol = plc_manager.get_man_req_protocol() # триггер формирование протокола в ручном режиме


            if trigger == True and not p1:
                logging.info(f"Обнаружен активный триггер., Длина : {length}, триггер : {trigger}, Run: : {lineRun}, manReq : {manReqProtocol}")

                #сброс триггера
                time.sleep(3)
                plc_manager.reset_trigger()
                plc_manager.lump_send_fault_plc()
                plc_manager.spark_send_fault_plc()

                replace_xlsx_with_template(blank_report,template_report)
                logging.info(f'меняем файл из {blank_report} -> {template_report}')
            p1=trigger

        except Exception as e:
            logging.error(f"Ошибка в основном потоке: {e}")
            time.sleep(1)  # Пауза перед повторной попыткой
