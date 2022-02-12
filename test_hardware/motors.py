

from pyrobot.gpio_mapping import WheelMotors

import time
import pigpio

from enum import IntEnum

class DecayMode(IntEnum):
    FAST = 0
    SLOW = 1

PWM_FREQ = 8_000
# max 8000Hz at default sample_rate (4us)
# https://abyz.me.uk/rpi/pigpio/python.html#set_PWM_frequency

gpio = pigpio.pi()

# https://e2e.ti.com/support/motor-drivers-group/motor-drivers/f/motor-drivers-forum/251780/drv8833-pwm-control
class WheelMotor:

    def __init__(self, pin_in1: int, pin_in2: int, enable_pin: int):
        self.pin1 = pin_in1
        self.pin2 = pin_in2
        self.pin_en = enable_pin

        self.pwm_decay_mode = DecayMode.SLOW

        gpio.set_mode(self.pin_en, pigpio.OUTPUT)

        for pin in (self.pin1, self.pin2):
            gpio.set_mode(pin, pigpio.OUTPUT)
            freq = gpio.set_PWM_frequency(pin, PWM_FREQ)
            print(freq)
            gpio.set_PWM_range(pin, 100)  # use % to set speed

    def enable(self):
        gpio.write(self.pin_en, 1)

    def disable(self):
        gpio.write(self.pin_en, 0)

    def set_speed(self, speed: int):
        """0 = MAX SPEED"""
        pin_pwm, pin_fix = (
            (self.pin1, self.pin2)
            if speed >= 0
            else (self.pin2, self.pin1)
        )

        gpio.set_PWM_dutycycle(pin_pwm, abs(speed))
        gpio.set_PWM_dutycycle(pin_fix, 100*self.pwm_decay_mode)

    def brake(self):
        """Slow decay."""
        gpio.set_PWM_dutycycle(self.pin1, 100)
        gpio.set_PWM_dutycycle(self.pin2, 100)

    def coast(self):
        """Fast decay."""
        gpio.set_PWM_dutycycle(self.pin1, 0)
        gpio.set_PWM_dutycycle(self.pin2, 0)


wheel_left = WheelMotor(
     WheelMotors.LEFT_1,
     WheelMotors.LEFT_2,
     WheelMotors.EN
)

wheel_left.set_speed(00)
wheel_left.enable()

time.sleep(2)
wheel_left.coast()
time.sleep(2)
wheel_left.set_speed(-0)

time.sleep(2)


wheel_left.disable()