
import asyncio

from .hardware.leds_sn3218 import SN3218



class RgbUnderlighting:

    # Underlighting LED locations
    LIGHT_FRONT_RIGHT = 0
    LIGHT_FRONT_LEFT = 1
    LIGHT_MIDDLE_LEFT = 2
    LIGHT_REAR_LEFT = 3
    LIGHT_REAR_RIGHT = 4
    LIGHT_MIDDLE_RIGHT = 5
    NUM_UNDERLIGHTS = 6


    def __init__(self):

        self.sn3218 = SN3218()

    
    async def flash(self, color= None):

        for k in range(0, 255, 8):
            values = [k]*18
            self.sn3218.set_intensity(values)
            await asyncio.sleep(.001)

        await asyncio.sleep(.001)

        for k in range(0, 255, 2):
            values = [255 - k]*18
            self.sn3218.set_intensity(values)
            await asyncio.sleep(.001)

        await asyncio.sleep(.001)
        self.sn3218.shutdown()