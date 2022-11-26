#!/usr/bin/env python3
# vuquangtrong.github.io
# see https://www.codeinsideout.com/blog/pi/stream-picamera-mjpeg/


import io
import time
import picamera
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Condition


class FrameBuffer(object):
    """
    FrameBuffer is a synchronized buffer which gets each frame and notifies to all waiting clients.
    It implements write() method to be used in picamera.start_recording()
    """

    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        """On new frame."""
        if buf.startswith(b"\xff\xd8"):
            with self.condition:
                self.buffer.seek(0)
                self.buffer.write(buf)
                self.buffer.truncate()
                self.frame = self.buffer.getvalue()
                # notify all other threads
                self.condition.notify_all()


class StreamingHandler(SimpleHTTPRequestHandler):
    """
    StreamingHandler extent http.server.SimpleHTTPRequestHandler class to handle mjpg file for live stream
    """

    def __init__(self, frames_buffer, *args):
        self.frames_buffer = frames_buffer
        print("New StreamingHandler, using frames_buffer=", frames_buffer)
        super().__init__(*args)

    def __del__(self):
        print("Remove StreamingHandler")

    def do_GET(self):
        if self.path == "/stream.mjpg":
            self.send_response(200)
            self.send_header("Age", 0)
            self.send_header("Cache-Control", "no-cache, private")
            self.send_header("Pragma", "no-cache")
            self.send_header(
                "Content-Type", "multipart/x-mixed-replace; boundary=FRAME"
            )
            self.end_headers()
            try:
                # tracking serving time
                start_time = time.time()
                frame_count = 0
                # endless stream
                while True:
                    with self.frames_buffer.condition:
                        # wait for a new frame
                        self.frames_buffer.condition.wait()
                        # it's available, pick it up
                        frame = self.frames_buffer.frame
                        # send it
                        self.wfile.write(b"--FRAME\r\n")
                        self.send_header("Content-Type", "image/jpeg")
                        self.send_header("Content-Length", len(frame))
                        self.end_headers()
                        self.wfile.write(frame)
                        self.wfile.write(b"\r\n")
                        # count frames
                        frame_count += 1
                        # calculate FPS every 5s
                        if (time.time() - start_time) > 5:
                            print("FPS: ", frame_count / (time.time() - start_time))
                            frame_count = 0
                            start_time = time.time()
            except Exception as e:
                print(f"Removed streaming client {self.client_address}, {str(e)}")
        else:
            # fallback to default handler
            print("GET", self.path)
            self.path = "../index.html"
            super().do_GET()

    #         self.wfile.write(b"""<html>    <body>
    #     <img src="stream.mjpg" />
    # </body></html>""")


def stream():

    with picamera.PiCamera(resolution="640x480", framerate=24) as camera:
        frame_buffer = FrameBuffer()
        camera.start_recording(frame_buffer, format="mjpeg")

        # run server
        try:
            address = ("", 8000)
            httpd = ThreadingHTTPServer(
                address, lambda *args: StreamingHandler(frame_buffer, *args)
            )
            httpd.serve_forever()
        finally:
            camera.stop_recording()


if __name__ == "__main__":
    stream()
