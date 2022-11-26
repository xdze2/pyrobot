from queue import Queue
from threading import Event, Thread
from typing import Union

import matplotlib.pyplot as plt
import numpy as np

from pyrobot.odometry import ImuAngle, MiceMvt, listen_imu, listen_the_mice


msg_queue = Queue()

def msg_callback(msg):
    msg_queue.put(msg)


run_event = Event()
run_event.set()

imu_thread = Thread(target=listen_imu, args=[msg_callback, run_event])
mice_thread = Thread(target=listen_the_mice, args=[msg_callback, run_event])

print("Start imu thread...")
imu_thread.start()
print("Start mice thread...")
mice_thread.start()




class RobotPosition:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.current_angle_rad = 0
        self.log = list()

    def update(self, msg: Union[ImuAngle, MiceMvt]):
        if isinstance(msg, ImuAngle):
            self.current_angle_rad = msg.angle * np.pi / 180
        elif isinstance(msg, MiceMvt):
            dx = np.cos(self.current_angle_rad) * msg.dx
            dy = np.sin(self.current_angle_rad) * msg.dy
            self.x += dx
            self.y += dy
            print("pos:", self.x, self.y)
            self.log.append((self.x, self.y))
        else:
            print(f"what? {msg}")


robot_position = RobotPosition()
while True:

    try:
        msg = msg_queue.get()
        robot_position.update(msg)

    except KeyboardInterrupt:
        print("exit, clear event (move the robot to exit...)")
        run_event.clear()
        mice_thread.join()
        print("mice thread is joined")
        imu_thread.join()
        print("imu thread is joined")
        break


plt.figure()
log = np.array(robot_position.log)
plt.plot(log[:, 0], log[:, 1])
plt.xlabel("x")
plt.ylabel("y")
plt.tight_layout()
graph_path = f"output/trajectory.png"
plt.savefig(graph_path)
print(f"Trajectory graph saved to {graph_path}")
