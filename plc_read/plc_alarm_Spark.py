# записываем в db7.dbx5.1 True
from config import  db_number, offset_trigger

def spark_send_fault_plc(plc):
    try:  # Читаем текущий байт
        byte_data = plc.db_read(db_number, offset_trigger +1, 1)
        current_byte = byte_data[0]

        new_byte = current_byte |(1 << 1)

        # Записываем измененный байт обратно в блок данных
        plc.db_write(db_number, offset_trigger +1, bytearray([new_byte]))

    except Exception as e:
        print( f'error : {e}')
