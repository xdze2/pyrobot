import subprocess as sp
import signal
import re

import time

args = "./cimu/bin/imuZ"


reg = re.compile(r"time:\s+([\d]+)\s+angle:\s+([-\d\.]+)")


def parse_stdout(line: str):

    if line.startswith("#") or line.startswith("offset"):
        print(line, end="")
    else:
        matchs = reg.findall(line)
        if matchs:
            timestamp = int(matchs[0][0])
            angle = float(matchs[0][1])
            print(f"angle={angle} deg.  dt={timestamp}us", time.time())
        else:
            print(f"regex error: {line}")


with sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE) as proc:
    print(f"popen {args}")

    while True:
        try:
            line = proc.stdout.readline()
            line = line.decode("utf-8")
            parse_stdout(line)

        except KeyboardInterrupt:
            print("Terminating...")
            proc.send_signal(signal.SIGINT)

            for k in range(10):
                line = proc.stdout.readline().decode("utf-8")
                print(line, end="")

            print("break while loop")
            break


print("exit")
