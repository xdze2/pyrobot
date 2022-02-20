

from pyrobot.hardware.sonar import UltraSoundSensor
from pyrobot.gpio_mapping import SonarGpio
import pigpio

gpio = pigpio.pi()

sensor = UltraSoundSensor(gpio_echo=SonarGpio.ECHO, gpio_trig=SonarGpio.TRIG, gpio=gpio)


print(f"sonar distance = {sensor.measure_cm()} cm")

