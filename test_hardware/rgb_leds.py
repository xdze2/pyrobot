import asyncio

from pyrobot.rgb_leds import RgbUnderlighting

underligts = RgbUnderlighting()





async def main():


    await underligts.flash()



asyncio.run(main())

