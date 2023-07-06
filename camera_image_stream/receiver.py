# Imports
from pynng import Pub0
import numpy as np
import cv2


# Constants
RASPBERRY_IP = "192.168.1.100"
RASPBERRY_PORT = 8000

PUB_ADDRESS = "ipc:///tmp/RAAI/camera_frame.ipc"

video_capture = cv2.VideoCapture(f"udp://{RASPBERRY_IP}:{RASPBERRY_PORT}", cv2.CAP_FFMPEG)
if not video_capture.read()[0]:
    video_capture = cv2.VideoCapture(f"tcp://{RASPBERRY_IP}:{RASPBERRY_PORT}", cv2.CAP_FFMPEG)

pub_sender = Pub0()
pub_sender.listen(PUB_ADDRESS)


# Main Loop
def main(show_preview: bool = False):
    """Receives the frame from the raspberry pi.

    Args:
        show_preview (bool): If True it will show the received frame from the raspberry pi.

    Raises:
        ConnectionError: If the connection has been interrupted and the next frame could not be read.
    """
    while True:
        success, frame = video_capture.read()

        if not success:
            raise ConnectionError("Could not read the next frame. Check the camera.")

        frame_np_array = np.array(frame)
        frame_bytes = frame_np_array.tobytes()
        pub_sender.send(frame_bytes)

        if show_preview:
            cv2.imshow("frame", frame)
            cv2.waitKey(1)


if __name__ == "__main__":
    main()
