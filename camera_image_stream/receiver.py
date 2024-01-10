"""Receives a video stream from a Raspberry Pi and publishes it to a pynng publisher."""
# Copyright (C) 2023, NG:ITL

from pathlib import Path
from json import load, dump

from pynng import Pub0
from jsonschema import validate
import numpy as np
import cv2


FILE_DIR = Path(__file__).parent
CONFIG_FILE_NAME = "camera_image_stream_config.json"


def create_config_file() -> None:
    """Creates a config file with default values."""
    with open(FILE_DIR / "templates/config.json", "r", encoding="utf-8") as template:
        with open(CONFIG_FILE_NAME, "x", encoding="utf-8") as config_file:
            dump(load(template), config_file, indent=4)


def main() -> None:
    """Receives a video stream from a Raspberry Pi and publishes it to a pynng publisher.

    Raises:
        ConnectionError: If the next frame could not be read from the video stream.
    """
    if not Path(CONFIG_FILE_NAME).is_file():
        create_config_file()

    with open(CONFIG_FILE_NAME, "r", encoding="utf-8") as config_file:
        config = load(config_file)

        with open(FILE_DIR / "schema/config_schema.json", "r", encoding="utf-8") as schema_file:
            validate(config, load(schema_file))

        camera_stream = config["pynng"]["publishers"]["camera_image_publisher"]
        raspberry_pi_config = config["raspberry_pi"]
        show_preview = config["show_preview"]

    video_capture = cv2.VideoCapture(f"udp://{raspberry_pi_config['ip']}:{raspberry_pi_config['port']}", cv2.CAP_FFMPEG)  # type: ignore[call-arg]
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
