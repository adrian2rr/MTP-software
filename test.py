import pytransciever

print("Init!")
pytransciever.py_spi_init()

PTX = 1
"""
    Tx pin:
    MOSI: 19
    MISO: 21
    SCLK: 23
    CSN:  24
    CE:   22
"""
PRX = 2
"""
    Tx pin:
    MOSI: 38
    MISO: 35
    SCLK: 40
    CSN:  36
    CE:   37
"""

DATA_TX = 1
DATA_RX = 2

tx = pytransciever.Transciever(PTX,DATA_TX)
rx = pytransciever.Transciever(PRX,DATA_TX)

tx.print_info()
rx.print_info()

rx.py_rx_mode()

tx.py_send_single_message(b'12345678901234567890123456789012')

# Funcion bloqueante implementar timout
#msg = rx.py_wait_single_message()

#print(msg)

print("End!")
pytransciever.py_spi_end()
