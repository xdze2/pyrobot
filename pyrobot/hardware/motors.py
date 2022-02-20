

import pigpio
from enum import IntEnum


class DecayMode(IntEnum):
    FAST = 0
    SLOW = 1


class WheelMotor:

    PWM_FREQ = 50
    # max 8000Hz at default sample_rate (5 us)
    # https://abyz.me.uk/rpi/pigpio/python.html#set_PWM_frequency

    # https://e2e.ti.com/support/motor-drivers-group/motor-drivers/f/motor-drivers-forum/251780/drv8833-pwm-control

    def __init__(self, pin_in1: int, pin_in2: int, enable_pin: int, gpio: pigpio.pi):
        self.pin1 = pin_in1
        self.pin2 = pin_in2
        self.pin_en = enable_pin
        self.gpio = gpio

        self.pwm_decay_mode = DecayMode.SLOW

        self.gpio.set_mode(self.pin_en, pigpio.OUTPUT)

        for pin in (self.pin1, self.pin2):
            self.gpio.set_mode(pin, pigpio.OUTPUT)
            freq = gpio.set_PWM_frequency(pin, self.PWM_FREQ)
            self.gpio.set_PWM_range(pin, 100)  # use % to set speed

    def set_speed(self, speed: int):
        """MAX SPEED = 100"""

        if not self.is_enable():
            self.enable()

        pin_pwm, pin_fix = (
            (self.pin1, self.pin2) if speed >= 0 else (self.pin2, self.pin1)
        )

        duty_cycle = max(0, 100 - abs(speed))
        self.gpio.set_PWM_dutycycle(pin_pwm, duty_cycle)
        self.gpio.set_PWM_dutycycle(pin_fix, 100 * self.pwm_decay_mode)

    def enable(self):
        self.gpio.write(self.pin_en, 1)

    def disable(self):
        self.gpio.write(self.pin_en, 0)

    def is_enable(self) -> bool:
        return self.gpio.read(self.pin_en)

    def brake(self):
        """Slow decay."""
        self.gpio.set_PWM_dutycycle(self.pin1, 100)
        self.gpio.set_PWM_dutycycle(self.pin2, 100)

    def coast(self):
        """Fast decay."""
        self.gpio.set_PWM_dutycycle(self.pin1, 0)
        self.gpio.set_PWM_dutycycle(self.pin2, 0)
