

import time

from threading import Thread

from pyrobot.drive import Mobility
from pyrobot.imu import Imu


import numpy as np
import matplotlib.pyplot as plt


mob = Mobility()

data = list()
sense = Imu(data)


th = Thread(
     target=sense.loop
)

th.start()

time.sleep(.2)
mob.drive(0, -70, 0.5)
time.sleep(.2)
mob.drive(0, 70, 1)
time.sleep(.2)

sense.run = False


data = np.array(sense.data)


plt.plot(data[:, 0], label='wx')
plt.plot(data[:, 1], label='wy')
plt.plot(data[:, 2], label='wz')
plt.legend()
plt.savefig('graph.png')