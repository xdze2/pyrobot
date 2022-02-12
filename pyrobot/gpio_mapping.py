

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


class WheelMotors(IntEnum):
    """Motor driver pins, via DRV8833PWP Dual H-Bridge."""
    EN = 26
    LEFT_P = 8
    LEFT_N = 11
    RIGHT_P = 10
    RIGHT_N = 9