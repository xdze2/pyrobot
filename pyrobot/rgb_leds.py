import asyncio
from typing import Tuple, NamedTuple
from .hardware.leds_sn3218 import SN3218

import colorsys



class RgbColor(NamedTuple):
    r: int
    g: int
    b: int

    def to_rgb(self) -> 'RgbColor':
        return self


class HsvColor(NamedTuple):
    h: int
    s: int
    v: int

    def to_rgb(self) -> RgbColor:
        return RgbColor(*(
            int(u*255)
            for u in colorsys.hsv_to_rgb(*(v/255 for v in self))
        ))


class RgbUnderlighting:

    # Underlighting LED locations

    LED_MAPPING = [
        "front_right",
        "front_left",
        "middle_left",
        "rear_left",
        "rear_right",
        "middle_right",
    ]

    def __init__(self):

        self.sn3218 = SN3218()

        # State
        self.intensity_values = self._ones(HsvColor(255, 0, 100))

    def _ones(self, hsv_color: HsvColor):
        intensities = [
            color
            for _led_name in self.LED_MAPPING
            for color in hsv_color.to_rgb()
        ]
        return intensities

    def set_color(self, color: HsvColor, led_id_pattern: str = ''):

        values = self._ones(color)
        self.sn3218.set_intensity(values)


    async def flash(self, hue: int = 0, saturation: int = 0):

        self.sn3218.start()
        for k in range(0, 255, 8):
            values = self._ones(HsvColor(hue, saturation, k))
            self.sn3218.set_intensity(values)
            await asyncio.sleep(0.001)

        await asyncio.sleep(0.001)

        for k in range(0, 255, 2):
            kbar = 255 - k
            values = self._ones(HsvColor(hue, saturation, kbar))
            self.sn3218.set_intensity(values)
            await asyncio.sleep(0.001)

        await asyncio.sleep(0.001)
        self.sn3218.shutdown()


    