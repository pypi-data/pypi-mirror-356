# /*****************************************************************************
# * | File        :	  epdconfig.py
# * | Author      :   Waveshare team
# * | Function    :   Hardware underlying interface
# * | Info        :
# *----------------
# * | This version:   V1.2
# * | Date        :   2022-10-29
# * | Info        :   
# ******************************************************************************
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import logging
import sys
import time
from periphery import GPIO, SPI

logger = logging.getLogger(__name__)


class RaspberryPi:
    # Pin definition
    # Luckfox Pico Pro
    # RST_PIN  = ("/dev/gpiochip1", 25)
    # DC_PIN   = ("/dev/gpiochip1", 24)
    # BUSY_PIN = ("/dev/gpiochip2", 8)

    # Luckfox Pico Mini
    RST_PIN  = ("/dev/gpiochip1", 19)
    DC_PIN   = ("/dev/gpiochip1", 20)
    BUSY_PIN = ("/dev/gpiochip1", 11)
    # CHUNK_SIZE = 4096 * 12  # 48KB chunks
    CHUNK_SIZE = 4096  # 48KB chunks


    def __init__(self):
        # Initialize GPIO pins
        self.GPIO_RST_PIN = GPIO(*self.RST_PIN, "out")
        self.GPIO_DC_PIN = GPIO(*self.DC_PIN, "out")
        self.GPIO_BUSY_PIN = GPIO(*self.BUSY_PIN, "in")
        
        # Initialize SPI
        self.SPI = SPI("/dev/spidev0.0", 0, 4_000_000)  # 4MHz

    def __del__(self):
        """Cleanup GPIO and SPI resources when object is destroyed"""
        try:
            logger.debug("Cleaning up GPIO and SPI resources...")
            self.module_exit()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    def _chunked_transfer(self, data):
        """Transfer data in chunks to prevent buffer overflows"""
        if isinstance(data, list):
            data = bytes(data)
        
        for i in range(0, len(data), self.CHUNK_SIZE):
            chunk = data[i:i + self.CHUNK_SIZE]
            self.SPI.transfer(chunk)

    def digital_write(self, pin, value):
        if pin == self.RST_PIN:
            self.GPIO_RST_PIN.write(bool(value))
        elif pin == self.DC_PIN:
            self.GPIO_DC_PIN.write(bool(value))
        # elif pin == self.PWR_PIN:
        #     self.GPIO_PWR_PIN.write(value)

    def digital_read(self, pin):
        if pin == self.BUSY_PIN:
            return self.GPIO_BUSY_PIN.read()
        return 0

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self._chunked_transfer(data)

    def spi_writebyte2(self, data):
        self._chunked_transfer(data)

    def module_init(self):
        # self.GPIO_PWR_PIN.write(True)
        return 0

    def module_exit(self):
        logger.debug("spi end")
        self.SPI.close()

        self.GPIO_RST_PIN.write(False)
        self.GPIO_DC_PIN.write(False)
        logger.debug("close 5V, Module enters 0 power consumption ...")
        
        self.GPIO_RST_PIN.close()
        self.GPIO_DC_PIN.close()
        self.GPIO_BUSY_PIN.close()

implementation = RaspberryPi()


for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))

### END OF FILE ###
