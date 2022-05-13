import zmq

# https://zguide.zeromq.org/docs/chapter2/#Pub-Sub-Message-Envelopes

def main():
    """ main method """

    # Prepare our context and publisher
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://localhost:5563")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"cam")

    while True:
        # Read envelope with address
        [address, contents] = subscriber.recv_multipart()
        print(f"[{address}] {contents}")

    # We never get here but clean up anyhow
    subscriber.close()
    context.term()


if __name__ == "__main__":
    main()