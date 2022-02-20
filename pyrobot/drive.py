import asyncio
import time

import pigpio

from pyrobot.hardware.motors import WheelMotor
from pyrobot.gpio_mapping import WheelMotorsGpio


class Mobility:
    def __init__(self):

        gpio = pigpio.pi()

        self.left_wheel = WheelMotor(
            WheelMotorsGpio.LEFT_2,  # <-- inverted
            WheelMotorsGpio.LEFT_1,
            WheelMotorsGpio.EN,
            gpio,
        )

        self.right_wheel = WheelMotor(
            WheelMotorsGpio.RIGHT_1, WheelMotorsGpio.RIGHT_2, WheelMotorsGpio.EN, gpio
        )

    def drive(self, speed: int, curve: int = 0):

        self.left_wheel.set_speed(speed + curve)
        self.right_wheel.set_speed(speed - curve)

    def stop(self):
        # await asyncio.sleep(duration_sec)
        self.left_wheel.coast()
        self.right_wheel.coast()

        self.left_wheel.disable()
        self.right_wheel.disable()
