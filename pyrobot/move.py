


from pyrobot.gpio_mapping import WheelMotorsGpio

import time
import pigpio

from enum import IntEnum
from pyrobot.drivers.motors import WheelMotor


gpio = pigpio.pi()


left_wheel = WheelMotor(
     WheelMotorsGpio.LEFT_2,   # <-- inverted
     WheelMotorsGpio.LEFT_1,
     WheelMotorsGpio.EN,
     gpio
)

right_wheel = WheelMotor(
     WheelMotorsGpio.RIGHT_1,
     WheelMotorsGpio.RIGHT_2,
     WheelMotorsGpio.EN,
     gpio
)
