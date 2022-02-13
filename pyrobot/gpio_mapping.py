

from enum import IntEnum


class SonarGpio(IntEnum):
    """HC-SR04 Ultrasound pins."""
    ECHO = 25
    TRIG = 13


class OnboardLEDGpio(IntEnum):
    """Onboard LEDs pins (next to each button)."""
    LED_A = 23
    LED_B = 22
    LED_X = 17
    LED_Y = 27


class WheelMotorsGpio(IntEnum):
    """Motor driver pins, via DRV8833PWP Dual H-Bridge."""
    EN = 26
    LEFT_1 = 11
    LEFT_2 = 8
    RIGHT_1 = 9
    RIGHT_2 = 10