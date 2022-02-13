

from pyrobot.gpio_mapping import WheelMotorsGpio

import time
import pigpio

from enum import IntEnum
from pyrobot.drivers.motors import WheelMotor


gpio = pigpio.pi()

wheel_left = WheelMotor(
     WheelMotorsGpio.LEFT_1,
     WheelMotorsGpio.LEFT_2,
     WheelMotorsGpio.EN,
     gpio
)

wheel_left.set_speed(100)
# wheel_left.enable()

time.sleep(2)
wheel_left.coast()
time.sleep(2)
wheel_left.set_speed(-100)

time.sleep(2)


wheel_left.disable()
