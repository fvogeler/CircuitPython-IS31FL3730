# SPDX-FileCopyrightText: Ferdinand Vogeler 2022
#
# SPDX-License-Identifier: MIT

"""
`circuitpyhon_is31fl3730.LTP305`
====================================================
CircuitPython driver for the IS31FL3730 charlieplex IC.
Library based on Pimoroni Python code.

Implementation for LTP305 modules

* Author(s): Ferdinand Vogeler
Implementation Notes
--------------------
**Hardware:**
* `Pimoroni LED Dot Matrix Breakout
  <https://shop.pimoroni.com/products/led-dot-matrix-breakout>`_
* `Pimoroni Micro Dot pHAT
  <https://shop.pimoroni.com/products/microdot-phat>`_
"""

from . import IS31FL3730
from .font import font

class LTP305(IS31FL3730):
    """
    LTP305 LED matrix driver (IS31FL3730 based).

    :param ~busio.I2C i2c: the connected i2c bus i2c_device
    :param int address: the device address; defaults to 0x61

    _buf_matrix_left = [
    # Row  7654321
        0b01111111,  # col 1, bottom = msb
        0b01111111,  # col 2
        0b01111111,  # col 3
        0b01111111,  # col 4
        0b01111111,  # col 5
        0b00000000,
        0b00000000,
        0b01000000   # bit 7 = decimal dot
    ]
    _buf_matrix_right = [
    # Col    12345
        0b00011111,  # row 1
        0b00011111,  # row 2
        0b00011111,  # row 3
        0b00011111,  # row 4
        0b00011111,  # row 5
        0b00011111,  # row 6
        0b10011111,  # row 7 + bit 8 = decimal dot
        0b00000000
    ]
    """

    def __init__(self, i2c, address=0x61, brightness=0.5):
        """Initialize for 2x LTP305 5x7 Matrix Driver
        :param address: i2c address, one of 0x61, 0x62 or 0x63 (default 0x61)
        :param brightness: LED brightness from 0.0 to 1.0 (default 0.5)
        """
        super().__init__(i2c, address)
        self.set_brightness(brightness)
        self.clear()

    def clear(self):
        """Clear both LED matrices.
        Must call .show() to display changes.
        """
        self._buf_matrix_left = [0 for _ in range(8)]
        self._buf_matrix_right = [0 for _ in range(8)]

    def set_brightness(self, brightness, update=False):
        """Set brightness of both LED matrices.
        :param brightnes: LED brightness from 0.0 to 1.0
        :param update: Push change to display immediately (otherwise you must call .show())
        """
        self._brightness = int(brightness * 127.0)
        self._brightness = min(127, max(0, self._brightness))
        if update:
            self._i2c_write_reg(self.CMD_BRIGHTNESS, bytes([self._brightness]))

    def set_pixel(self, x, y, c):
        """Set a single pixel on the matrix.
        :param x: x position from 0 to 9 (0-4 on left matrix, 5-9 on right)
        :param y: y position
        :param c: state on/off
        """
        if x < 5:  # Left Matrix
            if c:
                self._buf_matrix_left[x] |= (0b1 << y)
            else:
                self._buf_matrix_left[x] &= ~(0b1 << y)
        else:      # Right Matrix
            x -= 5
            if c:
                self._buf_matrix_right[y] |= (0b1 << x)
            else:
                self._buf_matrix_right[y] &= ~(0b1 << x)

    def set_decimal(self, left=None, right=None):
        """Set decimal of left and/or right matrix.
        :param left: State of left decimal dot
        :param right: State of right decimal dot
        """
        if left is not None:
            if left:
                self._buf_matrix_left[7] |= 0b01000000
            else:
                self._buf_matrix_left[7] &= 0b10111111
        if right is not None:
            if right:
                self._buf_matrix_right[6] |= 0b10000000
            else:
                self._buf_matrix_right[6] &= 0b01111111

    def set_character(self, x, char):
        """Set a single character.
        :param x: x position, 0 for left, 5 for right, or in between if you fancy
        :param char: string character or char ordinal
        """
        if type(char) is not int:
            char = ord(char)
        char = font[char]
        for cx in range(5):
            for cy in range(8):
                c = char[cx] & (0b1 << cy)
                self.set_pixel(x + cx, cy, c)

    def get_shape(self):
        """Set the width/height of the display."""
        return 10, 7

    def show(self):
        """Update the LED matrixes from the buffer."""
        self._i2c_write_reg(self.CMD_MATRIX_L, bytes(self._buf_matrix_left))
        self._i2c_write_reg(self.CMD_MATRIX_R, bytes(self._buf_matrix_right))
        self._i2c_write_reg(self.CMD_MODE, bytes([self.MODE]))
        self._i2c_write_reg(self.CMD_OPTIONS, bytes([self.OPTS]))
        self._i2c_write_reg(self.CMD_BRIGHTNESS, bytes([self._brightness]))
        self._i2c_write_reg(self.CMD_UPDATE, bytes([0x01]))
