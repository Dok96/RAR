#plcReadTrig.py
from config import  db_number, offset_trigger

def read_trigger_def(plc):

    try:
        # Читаем данные из ПЛК
        byte_data= plc.db_read(db_number,offset_trigger ,1 )
        # Извлекаем значение бита
        byte_value = byte_data[0]  # Первый (и единственный) байт из массива

        bit_value_trig= (byte_value >> 0) & 0x01  # Извлекаем бит 0
        bit_value_run = (byte_value >> 1) & 0x01 # Извлекаем бит 1
        bit_value_man = (byte_value >> 2) & 0x01 # Извлекаем бит 2


        trigger_report = bool(bit_value_trig) # триггер формирования протокола
        lineRun = bool(bit_value_run) # триггер линия в работе
        manReqProtocol = bool(bit_value_man) # триггер формирование протокола в ручном режиме

        return trigger_report, lineRun, manReqProtocol   # Возвращаем значение триггера

    except Exception as e:
        print(f'ошибка : {e}')
        return False, False, False  # Возвращаем значения по умолчанию в случае ошибки