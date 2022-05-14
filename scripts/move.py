

import time

from threading import Thread

from pyrobot.drive import Mobility
# from pyrobot.imu import Imu


# import numpy as np
# import matplotlib.pyplot as plt



import zmq


# Prepare our context and publisher
context = zmq.Context()
subscriber = context.socket(zmq.PAIR)
subscriber.bind("tcp://*:5564")
# subscriber.setsockopt(zmq.SUBSCRIBE, b"key")

mob = Mobility()
while True:
     # Read envelope with address
     key = subscriber.recv()
     print('->', key)

     if key == b'i':
          print('forward')
          mob.drive(70, 0)
          time.sleep(.2)
          mob.drive(0, 0)
     elif key == b'k':
          print('backward')
          mob.drive(-70, 0)
          time.sleep(.2)
          mob.drive(0, 0)      
     # [address, contents] = subscriber.recv()
     # print(f"[{address}] {contents}")
     

# mob = Mobility()

# data = list()
# sense = Imu(data)


# th = Thread(
#      target=sense.loop
# )

# th.start()

# time.sleep(.2)
# mob.drive(0, -70, 1)
# time.sleep(.2)
# mob.drive(0, 70, 1)
# time.sleep(.2)

# sense.run = False


# data = np.array(sense.data)

# plt.plot(np.cumsum(data[:, 0]), label='wx')
# plt.plot(np.cumsum(data[:, 1]), label='wy')
# plt.plot(np.cumsum(data[:, 2]), label='wz')
# plt.legend()
# plt.savefig('graph.png')