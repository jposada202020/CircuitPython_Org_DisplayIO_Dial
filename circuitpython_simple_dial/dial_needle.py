# SPDX-FileCopyrightText: 2021 Kevin Matocha, 2023 Jose David Montoya
#
# SPDX-License-Identifier: MIT
"""

`dial_needle`
================================================================================
A simple dial gauge widget for displaying graphical information.
modified from dial gauge by Kevin Matocha

* Author(s): Kevin Matocha, Jose David Montoya

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

import math
import displayio
import vectorio

# pylint: disable=too-many-lines, too-many-instance-attributes, too-many-arguments
# pylint: disable=too-many-locals, too-many-statements, attribute-defined-outside-init
# pylint: disable=unused-argument, unsubscriptable-object, undefined-variable, invalid-name


class needle:
    """
    Class needle

    :param dial_object: dial object for the needle to be drawn on
    :param int needle_width: needle width. Default to :const:`3`
    :param int needle_color: color value for the needle. Defaults to :const:`0x880000`
    :param int needle_pad: space between the dial circle and the needle. Defaults to :const:`10`
    :param bool limit_rotation: Set True to limit needle rotation to between the
     ``min_value`` and ``max_value``, set to `False` for unlimited rotation. Defaults to `True`
    :param bool needle_full: Set to True to show a full needle. Defaults to `False`

    :param float min_value: the minimum value displayed on the dial. Defaults to :const:`0.0`
    :param float max_value: the maximum value displayed the dial. Defaults to :const:`100.0`
    :param float value: the value to display (if None, defaults to ``min_value``)


    """

    def __init__(
        self,
        dial_object,
        needle_width=3,
        needle_pad=10,
        needle_full=False,
        needle_color=0x880000,
        limit_rotation=True,
        value=None,
        min_value=0.0,
        max_value=100.0,
    ):
        if needle_full:
            self._dial_half = 1
        else:
            self._dial_half = 0

        self._needle_width_requested = needle_width
        self._needle_color = needle_color
        self._needle_pad = needle_pad

        self._min_value = min_value
        self._max_value = max_value
        if value is None:
            self._value = self._min_value
        else:
            self._value = value

        self._dial_half = needle_full
        self._dial_center = dial_object._dial_center
        self._dial_radius = dial_object._dial_radius
        self._needle_width = needle_width

        self._needle_pad = needle_pad
        self._limit_rotation = limit_rotation

        self._needle_palette = displayio.Palette(1)
        self._needle_palette[0] = self._needle_color

        self._needle = vectorio.Polygon(
            points=[(100, 100), (100, 50), (50, 50), (50, 100)],
            pixel_shader=self._needle_palette,
            x=0,
            y=0,
        )
        self._update_needle(self._value)
        dial_object.append(self._needle)

    def _update_needle(self, value):
        if self._limit_rotation:  # constrain between min_value and max_value
            value = max(min(self._value, self._max_value), self._min_value)

        self._draw_position(
            value / (self._max_value - self._min_value)
        )  # convert to position (0.0 to 1.0)

    def _draw_position(self, position):
        # Get the position offset from the motion function
        angle_offset = (2 * math.pi / 360) * (-180 + 360 * position)

        d_x = (self._needle_width / 2) * math.cos(angle_offset)
        d_y = (self._needle_width / 2) * math.sin(angle_offset)

        x_0 = round(
            self._dial_center[0]
            - (
                (self._dial_radius - self._needle_pad)
                * math.sin(angle_offset)
                * self._dial_half
            )
            - d_x
        )
        y_0 = round(
            self._dial_center[1]
            + (
                (self._dial_radius - self._needle_pad)
                * math.cos(angle_offset)
                * self._dial_half
            )
            - d_y
        )

        x_1 = round(
            self._dial_center[0]
            - (
                (self._dial_radius - self._needle_pad)
                * math.sin(angle_offset)
                * self._dial_half
            )
            + d_x
        )
        y_1 = round(
            self._dial_center[1]
            + (
                (self._dial_radius - self._needle_pad)
                * math.cos(angle_offset)
                * self._dial_half
            )
            + d_y
        )

        x_2 = round(
            self._dial_center[0]
            + ((self._dial_radius - self._needle_pad) * math.sin(angle_offset))
            + d_x
        )
        y_2 = round(
            self._dial_center[1]
            - ((self._dial_radius - self._needle_pad) * math.cos(angle_offset))
            + d_y
        )

        x_3 = round(
            self._dial_center[0]
            + ((self._dial_radius - self._needle_pad) * math.sin(angle_offset))
            - d_x
        )
        y_3 = round(
            self._dial_center[1]
            - ((self._dial_radius - self._needle_pad) * math.cos(angle_offset))
            - d_y
        )

        self._needle.points = [(x_0, y_0), (x_1, y_1), (x_2, y_2), (x_3, y_3)]

    @property
    def value(self):
        """The dial's value."""
        return self._value

    @value.setter
    def value(self, new_value):
        if new_value != self._value:
            self._value = new_value
            self._update_needle(self._value)
