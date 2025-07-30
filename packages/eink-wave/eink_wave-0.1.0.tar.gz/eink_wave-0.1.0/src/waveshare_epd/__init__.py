"""
Waveshare E-Paper Display Library

A modernized version of the Waveshare e-paper library using python-periphery.
"""

__version__ = "0.1.0"
__author__ = "Waveshare Electronics (original), Modernized fork"

# Don't import modules at package level to avoid GPIO initialization
# Users should import specific modules as needed:
# from waveshare_epd.epd4in2_V2 import EPD

__all__ = [
    'epd4in2_V2',
    'epd2in13_V2', 
    'epd2in9_V2',
    'epd7in5_V2',
]
