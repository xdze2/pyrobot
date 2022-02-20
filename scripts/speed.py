

import asyncio

import time
import matplotlib.pyplot as plt
import numpy as np
import pigpio
from pyrobot.drive import Mobility
from pyrobot.hardware.sonar import UltraSoundSensor
from pyrobot.gpio_mapping import SonarGpio

gpio = pigpio.pi()

distance_sensor = UltraSoundSensor(gpio_echo=SonarGpio.ECHO, gpio_trig=SonarGpio.TRIG, gpio=gpio)


mob = Mobility()



data = []
async def measure_distance():
    for k in range(5):
        tic = time.perf_counter()
        distance = (tic,  distance_sensor.measure_cm(nbr_measure=1))
        print(time.perf_counter() - tic)
        data.append(distance)
        await asyncio.sleep(0.001)


def move():
    mob.drive(50, 0, 1)


async def main():

    task = asyncio.create_task(measure_distance())
    
    mob.drive(80, 0)
    await asyncio.sleep(3)
    mob.stop()
    # time.sleep(5)
    task.cancel()


asyncio.run(main())


print(len(data))
data = np.array(data)

time = data[:, 0] - data[0, 0]
distance = data[:, 1]

plt.plot(time, distance, label='wx')
plt.savefig('output/sonar_speed.png')

print('Fig saved.')