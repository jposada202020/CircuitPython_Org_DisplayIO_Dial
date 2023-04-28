# SPDX-FileCopyrightText: 2021 Kevin Matocha, 2023 Jose David Montoya
#
# SPDX-License-Identifier: MIT
"""

`simple_dial`
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

# pylint: disable=too-many-lines, too-many-instance-attributes, too-many-arguments
# pylint: disable=too-many-locals, too-many-statements, attribute-defined-outside-init
# pylint: disable=unused-argument, unsubscriptable-object, undefined-variable, invalid-name
# pylint: disable=invalid-unary-operand-type

import math
import displayio
from terminalio import FONT as terminalio_FONT
from adafruit_display_text import bitmap_label
import bitmaptools


class Dial(displayio.Group):
    """A dial widget.  The origin is set using ``x`` and ``y``.

    :param int x: pixel position
    :param int y: pixel position

    :param int width: requested width, in pixels
    :param int height: requested height, in pixels
    :param int padding: keep out padding amount around the border, in pixels,
     default is 12

    :param int tick_color: tick line color (24-bit hex value). Defaults to :const:`0xFFFFFF`
    :param int major_ticks: number of major ticks. Defaults to :const:`5`
    :param int major_tick_stroke: major tick line stroke width, in pixels. Defaults to 3
    :param int major_tick_length: major tick length, in pixels. Default to :const:`10`

    :param str major_tick_labels: array of strings for the major tick labels,
     default is ("0", "25", "50", "75", "100")
    :param float tick_label_scale: the scaling of the tick labels. Defaults to :const:`1.0`
    :param Font tick_label_font: font to be used for major tick labels, default
     is ``terminalio.FONT``
    :param int tick_label_color: color for the major tick labels. Defaults to :const:`0xFFFFFF`
    :param Boolean angle_tick_labels: set True to rotate the major tick labels to
     match the tick angle. Defaults to `True`

    :param int minor_ticks: number of minor ticks (per major tick). Defaults to :const:`5`
    :param int minor_tick_stroke: minor tick line stroke width, in pixels. Defaults to :const:`1`
    :param int minor_tick_length: minor tick length, in pixels. Defaults to :const:`5`

    :param int background_color: background color (RGB tuple
     or 24-bit hex value), set `None` for transparent, default is `None`

    """

    def __init__(
        self,
        x=100,
        y=100,
        width=100,
        height=100,
        padding=5,  # keepout amount around border, in pixels
        tick_color=0xFFFFFF,
        major_ticks=5,  # if int, the total number of major ticks
        major_tick_stroke=4,
        major_tick_length=10,
        major_tick_labels=(
            "0",
            "25",
            "50",
            "75",
        ),
        minor_tick_labels=None,
        minor_ticks=3,  # if int, the number of minor ticks per major tick
        minor_tick_stroke=1,
        minor_tick_length=5,
        tick_label_font=None,
        tick_label_color=0xFFFFFF,
        rotate_tick_labels=True,
        tick_label_scale=1.0,
        background_color=None,
        **kwargs,
    ):
        super().__init__(x=x, y=y, scale=1)

        self._background_color = background_color

        self._major_tick_labels = major_tick_labels
        self._minor_ticks_labels = minor_tick_labels

        self._tick_color = tick_color
        self._tick_label_color = tick_label_color
        if tick_label_font is None:
            self._tick_label_font = terminalio_FONT
        else:
            self._tick_label_font = tick_label_font
        self._tick_label_scale = tick_label_scale
        self._rotate_tick_labels = rotate_tick_labels

        self._major_ticks = major_ticks
        self._major_tick_stroke = major_tick_stroke
        self._major_tick_length = major_tick_length
        self._minor_ticks = minor_ticks
        self._minor_tick_stroke = minor_tick_stroke
        self._minor_tick_length = minor_tick_length

        self._padding = padding

        self._dial_center = None
        self._dial_radius = None

        self._initialize_dial(width, height)

    def _initialize_dial(self, width, height):

        # get the tick label font height
        self._font_height = self._get_font_height(
            font=self._tick_label_font, scale=self._tick_label_scale
        )

        # update the dial dimensions to fit inside the requested width and height
        self._adjust_dimensions(width, height)
        self._bounding_box = [0, 0, self._width, self._height]

        # create the dial palette and bitmaps
        self.dial_bitmap = displayio.Bitmap(self._width, self._height, 3)

        self.position_major_ticks = self.draw_ticks(
            tick_count=self._major_ticks,
            tick_stroke=self._major_tick_stroke,
            tick_length=self._major_tick_length,
        )

        temporal_position_minor_ticks = self.draw_ticks(
            tick_count=self._minor_ticks * (self._major_ticks - 1) + 1,
            tick_stroke=self._minor_tick_stroke,
            tick_length=self._minor_tick_length,
        )
        self.position_minor_ticks = []
        for element in temporal_position_minor_ticks:
            if element not in self.position_major_ticks:
                self.position_minor_ticks.append(element)

        self.draw_labels(self.position_major_ticks, self._major_tick_labels)
        if self._minor_ticks_labels:
            self.draw_labels(self.position_minor_ticks, self._minor_ticks_labels)

        self.dial_palette = displayio.Palette(4)
        if self._background_color is None:
            self.dial_palette.make_transparent(0)
            self.dial_palette[0] = 0x000000
        else:
            self.dial_palette[0] = self._background_color
        self.dial_palette[1] = self._tick_label_color
        self.dial_palette[2] = self._tick_color

        # create the dial tilegrid and append to the self Widget->Group
        self.dial_tilegrid = displayio.TileGrid(
            self.dial_bitmap, pixel_shader=self.dial_palette
        )
        self.append(self.dial_tilegrid)

        self._draw_circle()
        # For CP version 8.1
        # bitmaptools.draw_circle(self.dial_bitmap, self._dial_center[0],
        # self._dial_center[1], self._dial_radius, 1)

    def _draw_circle(self):

        x = 0
        y = self._dial_radius
        d = 3 - 2 * self._dial_radius

        while x <= y:
            self.dial_bitmap[x + self._dial_center[0], y + self._dial_center[1]] = 1
            self.dial_bitmap[-x + self._dial_center[0], -y + self._dial_center[1]] = 1
            self.dial_bitmap[x + self._dial_center[0], -y + self._dial_center[1]] = 1
            self.dial_bitmap[-x + self._dial_center[0], y + self._dial_center[1]] = 1
            self.dial_bitmap[y + self._dial_center[0], x + self._dial_center[1]] = 1
            self.dial_bitmap[-y + self._dial_center[0], x + self._dial_center[1]] = 1
            self.dial_bitmap[-y + self._dial_center[0], -x + self._dial_center[1]] = 1
            self.dial_bitmap[y + self._dial_center[0], -x + self._dial_center[1]] = 1

            if d <= 0:
                d = d + (4 * x) + 6
            else:
                d = d + 4 * (x - y) + 10
                y = y - 1
            x = x + 1

    def _adjust_dimensions(self, width, height):

        # calculate the pixel dimension to fit within width/height (including padding)
        if (width - 2 * self._padding < 0) or (height - 2 * self._padding < 0):
            raise ValueError("Width, height, or padding size makes zero sized box")

        self._width = width
        self._height = math.ceil(width - 2 * self._padding) + (2 * self._padding)
        radius = round((width - 2 * self._padding) / 2)

        center_x = round(0.5 * radius * 2) + self._padding
        center_y = round(0.5 * radius * 2) + self._padding
        self._dial_center = (center_x, center_y)
        self._dial_radius = radius

    def _get_font_height(self, font, scale):
        if (self._major_tick_labels == []) or (font is None):
            font_height = 0
        else:
            if hasattr(font, "get_bounding_box"):
                font_height = int(scale * font.get_bounding_box()[1])
            elif hasattr(font, "ascent"):
                font_height = int(scale * font.ascent + font.ascent)
        return font_height

    def draw_ticks(self, tick_count, tick_stroke, tick_length):
        """Helper function for drawing ticks on the dial widget.  Can be used to
        customize the dial face.

        :param int tick_count: number of ticks to be drawn
        :param int tick_stroke: the pixel width of the line used to draw the tick

        """
        angle_positions = []
        if tick_count <= 1:
            pass
        else:
            tick_bitmap = displayio.Bitmap(
                tick_stroke, tick_length, 3
            )  # make a tick line bitmap for blitting
            tick_bitmap.fill(2)
            for i in range(tick_count):
                this_angle = round(
                    (-180 + ((i * 360 / (tick_count - 1)))) * (2 * math.pi / 360),
                    4,
                )  # in radians
                angle_positions.append(this_angle)
                target_position_x = self._dial_center[0] + self._dial_radius * math.sin(
                    this_angle
                )
                target_position_y = self._dial_center[1] - self._dial_radius * math.cos(
                    this_angle
                )

                bitmaptools.rotozoom(
                    self.dial_bitmap,
                    ox=round(target_position_x),
                    oy=round(target_position_y),
                    source_bitmap=tick_bitmap,
                    px=round(tick_bitmap.width / 2),
                    py=0,
                    angle=this_angle,  # in radians
                )
        return angle_positions

    def draw_labels(self, positions, labels):
        """Helper function for drawing text labels on the dial widget.  Can be used
        to customize the dial face.

        """

        label_count = len(positions)

        for i, this_label_text in enumerate(labels):
            if i >= label_count:
                break
            temp_label = bitmap_label.Label(
                self._tick_label_font, text=this_label_text
            )  # make a tick line bitmap for blitting

            this_angle = positions[i]

            target_position_x = self._dial_center[0] + (
                self._dial_radius + self._font_height // 2
            ) * math.sin(this_angle)
            target_position_y = self._dial_center[1] - (
                self._dial_radius + self._font_height // 2
            ) * math.cos(this_angle)

            if not self._rotate_tick_labels:
                this_angle = 0

            bitmaptools.rotozoom(
                self.dial_bitmap,
                ox=round(target_position_x),
                oy=round(target_position_y),
                source_bitmap=temp_label.bitmap,
                px=round(temp_label.bitmap.width // 2),
                py=round(temp_label.bitmap.height // 2),
                angle=this_angle,
                scale=self._tick_label_scale,
            )
