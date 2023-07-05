# Imports
from pynng import Pub0
import numpy as np
import cv2


# Constants
RASPBERRY_IP = "192.168.1.100"
RASPBERRY_PORT = 8000

VIDEO_CAPTURE = cv2.VideoCapture(f"udp://{RASPBERRY_IP}:{RASPBERRY_PORT}", cv2.CAP_FFMPEG)
if not VIDEO_CAPTURE.read()[0]:
    VIDEO_CAPTURE = cv2.VideoCapture(f"tcp://{RASPBERRY_IP}:{RASPBERRY_PORT}", cv2.CAP_FFMPEG)

SHOW_PREVIEW = False

PUB_ADDRESS = "ipc:///tmp/RAAI/camera_frame.ipc"
PUB_SENDER = Pub0()
PUB_SENDER.listen(PUB_ADDRESS)


# Main Loop
def main():
    while True:
        success, frame = VIDEO_CAPTURE.read()

        if not success:
            raise ConnectionError("Could not read the next frame. Check the camera.")

        frame_np_array = np.array(frame)
        frame_bytes = frame_np_array.tobytes()
        PUB_SENDER.send(frame_bytes)

        if SHOW_PREVIEW:
            cv2.imshow("frame", frame)
            cv2.waitKey(1)


if __name__ == "__main__":
    main()
