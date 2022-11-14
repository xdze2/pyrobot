import time
import numpy as np
import pigpio

from pyrobot.drive import Mobility
from pyrobot.gpio_mapping import SonarGpio
from pyrobot.hardware.sonar import UltraSoundSensor

# from pyrobot.rgb_leds import ColorMap, HsvColor, RgbUnderlighting

gpio = pigpio.pi()

distance_sensor = UltraSoundSensor(
    gpio_echo=SonarGpio.ECHO, gpio_trig=SonarGpio.TRIG, gpio=gpio
)

move = Mobility()


def go_forward(speed=70, duration=0.5):
    print(f"> go forward for dist {speed*duration}")
    move.drive(speed, 0)
    time.sleep(duration)
    move.stop()


def turn_right(speed=70, duration=1):
    print(f"> turn {speed} {duration}")
    move.drive(0, speed)
    time.sleep(duration)
    move.stop()


print("start")
for k in range(100):
    distance = distance_sensor.measure_cm()
    print(f"distance: {distance}")

    if distance > 40:
        go_forward()
    else:
        turn_right()

print("done")
