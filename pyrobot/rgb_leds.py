import asyncio
from typing import Tuple, NamedTuple, List
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
        self.led_colors = [
            HsvColor(0, 0, 0)
            for _name in self.LED_MAPPING
        ]

    def _ones(self, hsv_color: HsvColor):
        return [
            hsv_color for _led_name in self.LED_MAPPING
        ]

    def change_color(self, color: HsvColor, led_id_pattern: str = ''):
        """Select led."""
        colors = [
            (color if led_id_pattern in name else ancient_color)
            for name, ancient_color in zip(self.LED_MAPPING, self.led_colors)
        ]
        self._set_colors(colors)
        
    def turn_off(self):
        self.change_color(HsvColor(0, 0, 0), '')
        self.sn3218.shutdown()

    def _set_colors(self, color_values: List[RgbColor]):
        """Keep color state."""
        self.led_colors = color_values
        
        values = [
            individuel_color
            for color in self.led_colors
            for individuel_color in color.to_rgb()
        ]
        self.sn3218.set_intensity(values)

    def print_state(self):
        lines = (
            f"{name:>12}: {color}"
            for name, color in zip(self.LED_MAPPING, self.led_colors)
        )
        print('\n'.join(lines))

    async def flash(self, hue: int = 0, saturation: int = 0):

        self.sn3218.start()
        for k in range(0, 255, 8):
            values = self._ones(HsvColor(hue, saturation, k))
            self._set_colors(values)
            await asyncio.sleep(0.001)

        await asyncio.sleep(0.001)

        for k in range(0, 255, 2):
            kbar = 255 - k
            values = self._ones(HsvColor(hue, saturation, kbar))
            self._set_colors(values)
            await asyncio.sleep(0.001)

        await asyncio.sleep(0.001)
        self.sn3218.shutdown()


