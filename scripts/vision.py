import io
import struct
import time
import picamera
import time
import zmq




def main():
    """main method"""

    # Prepare our context and publisher
    context = zmq.Context()
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5563")


    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)
        camera.framerate = 30
        time.sleep(2)
        start = time.time()
        count = 0
        stream = io.BytesIO()
        # Use the video-port for captures...
        for foo in camera.capture_continuous(stream, "jpeg", use_video_port=True):
            stream.seek(0)
            publisher.send_multipart([b"cam", stream.read()])

            count += 1
            if time.time() - start > 30:
                break
            stream.seek(0)
            stream.truncate()
   
            print('pub')



    # We never get here but clean up anyhow
    publisher.close()
    context.term()


if __name__ == "__main__":
    main()





