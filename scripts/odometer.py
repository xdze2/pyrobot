from pyrobot.odometry import listen_imu, listen_the_mice, ImuAngle, MiceMvt


from threading import Thread, Event
from queue import Queue

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

while True:

    try:
        msq = msg_queue.get()
        print(msq)

    except KeyboardInterrupt:
        print("exit, clear event (move the robot to exit...)")
        run_event.clear()
        mice_thread.join()
        print("mice thread is joined")
        imu_thread.join()
        print("imu thread is joined")
        exit()
