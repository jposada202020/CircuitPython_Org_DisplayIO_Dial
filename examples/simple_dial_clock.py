# SPDX-FileCopyrightText: 2023 Neradoc
#
# SPDX-License-Identifier: MIT

import time
import board
import displayio
import terminalio
from circuitpython_simple_dial.simple_dial import Dial
from circuitpython_simple_dial.dial_needle import needle


display = board.DISPLAY

# Create a Dial widget
width = height = int(min(display.width, display.height) * 0.9)
my_dial = Dial(
    x=display.width // 2 - width // 2,  # set x-position
    y=display.height // 2 - height // 2,  # set y-position
    width=width,  # requested width of the dial
    height=height,  # requested height of the dial
    tick_label_font=terminalio.FONT,  # the font used for the tick labels
    needle_full=False,
    padding=24,  # add 12 pixels around the dial to make room for labels
    tick_label_scale=2,
    major_tick_labels=(
        "6",
        "9",
        "12",
        "3",
    ),
    minor_tick_labels=(
        "7",
        "8",
        "10",
        "11",
        "1",
        "2",
        "4",
        "5",
    ),
)

needle_hour = needle(
    my_dial,
    value=0,
    needle_color=0xFF0000,
    needle_width=5,
    needle_pad=30,
    min_value=0,
    max_value=12,
)
needle_min = needle(
    my_dial, value=0, needle_color=0xFF8000, needle_width=5, min_value=0, max_value=60
)
needle_sec = needle(
    my_dial, value=0, needle_color=0xFFFFFF, needle_width=2, min_value=0, max_value=60
)

my_group = displayio.Group()
my_group.append(my_dial)

display.show(my_group)

while True:
    now = time.localtime()
    needle_hour.value = (now.tm_hour + 7) % 12
    needle_min.value = (now.tm_min + 30) % 60
    needle_sec.value = (now.tm_sec + 30) % 60
    display.refresh()
