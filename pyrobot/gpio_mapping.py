

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