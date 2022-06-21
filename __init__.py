# SPDX-FileCopyrightText: Ferdinand Vogeler 2022
#
# SPDX-License-Identifier: MIT

"""
`circuitpyhon_is31fl3730`
====================================================
CircuitPython driver for the IS31FL3730 charlieplex IC.
Library based on Pimoroni Python code.
* Author(s): Ferdinand Vogeler
Implementation Notes
--------------------
**Hardware:**
* `Pimoroni LED Dot Matrix Breakout
  <https://shop.pimoroni.com/products/led-dot-matrix-breakout>`_
* `Pimoroni Micro Dot pHAT
  <https://shop.pimoroni.com/products/microdot-phat>`_
"""

# imports
from micropython import const
from adafruit_bus_device.i2c_device import I2CDevice

__version__ = "0.0.1"
__repo__ = "https://https://github.com/fvogeler/CircuitPython-IS31FL3730.git"



class IS31FL3730:
    """
    The IS31FL3730 main class for this chip.

    :param ~busio.I2C i2c: the connected i2c bus i2c_device
    :param int address: the device address; defaults to 0x61
    """

    MODE = const(0b00011000)
    OPTS = const(0b00001110)  # 1110 = 35mA, 0000 = 40mA

    CMD_BRIGHTNESS = const(0x19)
    CMD_MODE = const(0x00)
    CMD_UPDATE = const(0x0C)
    CMD_OPTIONS = const(0x0D)

    CMD_MATRIX_L = const(0x0E)
    CMD_MATRIX_R = const(0x01)

    def __init__(self, i2c, address=0x61):
        """Initialize for 2x LTP305 5x7 Matrix Driver
        :param address: i2c address, one of 0x61, 0x62 or 0x63 (default 0x61)
        :param brightness: LED brightness from 0.0 to 1.0 (default 0.5)
        """
        self.i2c_device = I2CDevice(i2c, address)

    def _i2c_write_reg(self, reg, data):
        # Write a contiguous block of data (bytearray) starting at the
        # specified I2C register address (register passed as argument).
        self._i2c_write_block(bytes([reg]) + data)

    def _i2c_write_block(self, data):
        # Write a buffer of data (byte array) to the specified I2C register
        # address.
        with self.i2c_device as i2c:
            i2c.write(data)
