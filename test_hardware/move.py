

from pyrobot.gpio_mapping import WheelMotorsGpio

import time
import pigpio

from enum import IntEnum
from pyrobot.drivers.motors import WheelMotor


gpio = pigpio.pi()

left_wheel = WheelMotor(
     WheelMotorsGpio.LEFT_2,   # inverted
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


def drive(speed: int, curve: int = 0):
 
     left_wheel.set_speed(speed + curve)
     right_wheel.set_speed(speed - curve)

     time.sleep(1)
     left_wheel.coast()

     left_wheel.disable()
     right_wheel.disable()


drive(0, -60)