# SPDX-FileCopyrightText: 2023 Jose David Montoya
#
# SPDX-License-Identifier: MIT

import time
import board
import displayio
import terminalio
from simple_dial import Dial


display = board.DISPLAY

# Create a Dial widget
my_dial = Dial(
    x=100,  # set x-position
    y=120,  # set y-position
    width=150,  # requested width of the dial
    height=150,  # requested height of the dial
    padding=12,  # add 12 pixels around the dial to make room for labels
    min_value=0,  # set the minimum value shown on the dial
    max_value=100,  # set the maximum value shown on the dial
    tick_label_font=terminalio.FONT,  # the font used for the tick labels
    needle_full=True,
)

my_group = displayio.Group()
my_group.append(my_dial)

display.show(my_group)  # add high level Group to the display

step_size = 1

for this_value in range(1, 100 + 1, step_size):
    my_dial.value = this_value
    display.refresh()  # force the display to refresh
time.sleep(0.5)

# run the dial from maximum to minimum
for this_value in range(100, 1 - 1, -step_size):
    my_dial.value = this_value
    display.refresh()  # force the display to refresh
time.sleep(0.5)
