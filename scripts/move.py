import zmq

from pyrobot.drive import Mobility


"""
Client ctrl robot movement.
To use with remote_ctrl.py on a host PC.
"""

# Prepare our context and publisher
context = zmq.Context()
subscriber = context.socket(zmq.PAIR)
subscriber.setsockopt(zmq.LINGER, 0)
url = "tcp://*:5564"
subscriber.bind(url)
print(f"Bind to {url}...")

mob = Mobility()
mob.drive(0, 0)
while True:
    # Read envelope with address
    state = subscriber.recv().decode("utf-8")

    speed, curve = 0, 0
    if "i" in state:
        speed += 70

    if "k" in state:
        speed += -70
    
    if "j" in state:
        curve += -100

    if "l" in state:
        curve += +100

    print(f"speed:{speed:> 4d}  curve:{curve:> 4d}   [ {state} ]")
    mob.drive(speed, curve)

