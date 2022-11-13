import time
from threading import Thread

import zmq
from pyrobot.drive import Mobility


# Prepare our context and publisher
context = zmq.Context()
subscriber = context.socket(zmq.PAIR)
subscriber.setsockopt(zmq.LINGER, 0)
subscriber.bind("tcp://*:5564")
# subscriber.setsockopt(zmq.SUBSCRIBE, b"key")


mob = Mobility()
mob.drive(0, 0)
while True:
    # Read envelope with address
    state = subscriber.recv().decode("utf-8")
    print("->", state)

    if "i" in state:
        speed = 70
    elif "k" in state:
        speed = -70
    else:
        speed = 0

    if "j" in state:
        curve = -70
    elif "l" in state:
        curve = +70
    else:
        curve = 0

    print(f"speed:{speed}  curve:{curve}")
    mob.drive(speed, curve)

    # if key == b'i':
    #      print('forward')
    #      mob.drive(70, 0)
    #      # time.sleep(.2)
    #      # mob.drive(0, 0)
    # elif key == b'k':
    #      print('backward')
    #      mob.drive(-70, 0)
    #      time.sleep(.2)
    #      mob.drive(0, 0)
    # else:
    #      print('stop')
    #      mob.drive(0, 0)
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
