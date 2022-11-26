import struct
import subprocess as sp
import signal
import re

from typing import Callable
import time

from collections import namedtuple

from threading import Event

MiceMvt = namedtuple("MiceMvt", ["time", "dx", "dy"])
ImuAngle = namedtuple("ImuAngle", ["time", "angle", "time_us"])


def listen_the_mice(callback: Callable[[MiceMvt], None], run_event: Event) -> None:
    """Get mice movement."""
    with open("/dev/input/mice", "rb") as f:
        print("Listen mice...")
        while run_event.is_set():
            buf = f.read(3)
            # see: https://thehackerdiary.wordpress.com/2017/04/21/exploring-devinput-1/
            # button = ord(str(buf[0])[0])
            # bLeft = button & 0x1
            # bMiddle = (button & 0x4) > 0
            # bRight = (button & 0x2) > 0
            dx, dy = struct.unpack("bb", buf[1:])
            callback(MiceMvt(time.time(), dx, dy))

    print("done")


IMU_EXEC = "./cimu/bin/imuZ"
STDOUT_PATTERN = re.compile(r"time:\s+([\d]+)\s+angle:\s+([-\d\.]+)")


def parse_stdout(line: str) -> ImuAngle:
    if line.startswith("#") or line.startswith("offset"):
        print(line, end="")
        return None
    else:
        matchs = STDOUT_PATTERN.findall(line)
        if matchs:
            timestamp = int(matchs[0][0])
            angle = float(matchs[0][1])
            return ImuAngle(time.time(), angle, timestamp)
        else:
            print(f"regex error: {line}")
            return None


def listen_imu(callback: Callable[[ImuAngle], None], run_event: Event) -> None:
    with sp.Popen(IMU_EXEC, stdout=sp.PIPE, stderr=None) as proc:
        print(f"popen {IMU_EXEC}")

        while run_event.is_set():
            try:
                line = proc.stdout.readline()
                line = line.decode("utf-8")
                imu_angle = parse_stdout(line)
                if imu_angle is not None:
                    callback(imu_angle)

            except KeyboardInterrupt:
                break

        print("Terminating...")
        proc.send_signal(signal.SIGINT)
        lines = proc.stdout.read().decode("utf-8")
        print(lines, end="")
