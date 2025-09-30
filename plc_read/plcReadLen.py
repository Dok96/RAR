#plcReadLen.py
import snap7.util

from config import db_number, offset_len

def read_len(plc):
    try:
        data=plc.db_read(db_number,offset_len,4)
        len_cable=snap7.util.get_real(data,0) # получаем длину
        return len_cable

    except Exception as e:
        print(f'Error : {e}')
        return None

