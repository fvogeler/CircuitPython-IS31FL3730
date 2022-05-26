import board
import busio
import time
from circuitpython_is31fl3730 import IS31FL3731

i2c = busio.I2C(board.GP19, board.GP18)

matrix = IS31FL3731(i2c)
decimal_l = False
decimal_r = True
matrix.set_decimal(decimal_l, decimal_r)
matrix.show()

while True:
    for n in range(10):
        matrix.set_character(0, str(n))
        matrix.set_character(5, 'abcdefghij'[n])
        decimal_l, decimal_r = decimal_r, decimal_l
        matrix.set_decimal(decimal_l, decimal_r)
        matrix.show()
        time.sleep(0.2)