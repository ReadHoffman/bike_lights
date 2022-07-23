# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
from defs import *
# from rotary_encoder_switch import *
import colorsys

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D21

# The number of NeoPixels
num_pixels = 73

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait=0.001):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


def light_test():
    try:
        while True:

            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((255, 0, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((255, 0, 0, 0))
            pixels.show()
            time.sleep(1)

            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 255, 0))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 255, 0, 0))
            pixels.show()
            time.sleep(1)

            # Comment this line out if you have RGBW/GRBW NeoPixels
            pixels.fill((0, 0, 255))
            # Uncomment this line if you have RGBW/GRBW NeoPixels
            # pixels.fill((0, 0, 255, 0))
            pixels.show()
            time.sleep(1)

            rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
            
    except KeyboardInterrupt:
        pixels.fill((0, 0, 0))
        pixels.show()

top_tube_up = list(range(0,17))
top_tube_up_rev = list(reversed(top_tube_up))
top_tube_down = list(range(17,44))
top_tube_down_rev = list(reversed(top_tube_down))
down_tube_down = list(range(44,73))
down_tube_down_rev = list(reversed(down_tube_down))
all_sections = [top_tube_up,top_tube_down,down_tube_down]
all_sections_back_to_front = [top_tube_up_rev,top_tube_down,down_tube_down_rev]
max_section_len = max(len(x) for x in all_sections)

color_range = []
for i in range(max_section_len):
    rgb = colorsys.hsv_to_rgb(i / 90., 1.0, 1.0)
    color_range.append([round(255*x) for x in rgb])
# color_range = list(Color("red").range_to(Color("green"),28))

def rainbow_cycle(wait=0.001):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
    time.sleep(wait)

def all_green():
    pixels.fill((0, 255, 0))
    pixels.show()
    
def flashing_red(delay=1):
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(delay)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(delay)

def accellerate(delay=.04,break_len = .5):
    for i in range(max_section_len):
        color = color_range[i]
        for section in all_sections_back_to_front:
            if i < len(section):
                pixels[section[i]] = color
        pixels.show()
        time.sleep(delay)
    time.sleep(break_len)    
    pixels.fill((0, 0, 0))
    pixels.show()

modes = [accellerate,rainbow_cycle, all_green , flashing_red ]
modes_len = len(modes)