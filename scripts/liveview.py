import time

import cv2
import numpy as np
import zmq

# https://zguide.zeromq.org/docs/chapter2/#Pub-Sub-Message-Envelopes


def main():
    """main method"""
    ip_address = "192.168.1.72"

    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect(f"tcp://{ip_address}:5563")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"cam")

    while True:
        [_address, contents] = subscriber.recv_multipart()
        show(contents)

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


cv2.namedWindow("liveview")


def show(jpeg_frame):

    img = cv2.imdecode(
        np.frombuffer(jpeg_frame, dtype=np.uint8), cv2.IMREAD_UNCHANGED
    )

    cv2.imshow("liveview", img)
    if cv2.waitKey(1) == ord("q"):
        print("exit")
        cv2.destroyAllWindows()
        exit()


if __name__ == "__main__":
    main()
