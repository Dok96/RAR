#plcReadTrig.py
from config import  db_number
from config import offset_trigger

def read_trigger_def(plc):

    try:
        # Читаем данные из ПЛК
        byte_data= hours_data = plc.db_read(db_number,offset_trigger ,1 )
        # Извлекаем значение бита
        byte_value = byte_data[0]  # Первый (и единственный) байт из массива
        bit_value= (byte_value >> 0) & 0x01  # Извлекаем бит 0

        trigger_report = bool(bit_value)

        return trigger_report  # Возвращаем значение триггера

    except Exception as e:
        print(f'ошибка : {e}')