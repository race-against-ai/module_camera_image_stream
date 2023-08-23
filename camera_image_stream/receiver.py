# Imports
from pathlib import Path
from pynng import Pub0
from json import load
import numpy as np
import cv2


def main() -> None:
    config_path = Path().cwd() / "camera_image_stream_config.json"
    with open(config_path, "r") as config_file:
        config = load(config_file)
        camera_stream = config["pynng"]["publishers"]["camera_image_publisher"]
        raspberry_pi_config = config["raspberry_pi"]
        show_preview = config["show_preview"]

    video_capture = cv2.VideoCapture(f"udp://{raspberry_pi_config['ip']}:{raspberry_pi_config['port']}", cv2.CAP_FFMPEG)
    pub_sender = Pub0(listen=camera_stream["address"])

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
