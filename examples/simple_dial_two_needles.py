# SPDX-FileCopyrightText: 2023 Jose David Montoya
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
my_dial = Dial(
    x=40,  # set x-position
    y=40,  # set y-position
    width=150,  # requested width of the dial
    height=150,  # requested height of the dial
    padding=12,  # add 12 pixels around the dial to make room for labels
    tick_label_font=terminalio.FONT,  # the font used for the tick labels
    needle_full=False,
)

my_needle = needle(my_dial, value=30)
my_needle2 = needle(my_dial, value=60)

my_group = displayio.Group()
my_group.append(my_dial)


display.show(my_group)  # add high level Group to the display

step_size = 1

for this_value in range(1, 100 + 1, step_size):
    my_needle.value = this_value
    for this_other_value in range(1, 100, step_size):
        my_needle2.value = this_other_value
        display.refresh()
    display.refresh()  # force the display to refresh
time.sleep(0.5)
