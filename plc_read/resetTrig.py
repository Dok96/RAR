#resetTrig.py

from config import  db_number
from config import offset_trigger

def res_trigger(plc):
    try:  # Читаем текущий байт
        byte_data = plc.db_read(db_number, offset_trigger, 1)
        current_byte = byte_data[0]
        # Сбрасываем бит 0 в 0
        new_byte = current_byte & ~(1 << 0)

        # Записываем измененный байт обратно в блок данных
        plc.db_write(db_number, offset_trigger, bytearray([new_byte]))

    except Exception as e:
        print( f'error : {e}')
