# RAAI Module Camera Image Stream

## Overview

### Getting images

To take the pictures from the camera and get them read to transfer "libcamera-vid" is being used.

### Sending images to the PC

To send the images to the PC it uses a UDP-Multicast on "239.255.0.1:8000".

(standard setting for module; change in the [config](camera_image_stream_config.json) and on the raspberry pi under `/usr/local/bin/start_camera_stream.sh` replace `239.0.0.1:8000` with the new address)

### Sending images to other components

To send the images to other components it uses a pynng socket on "ipc:///tmp/camera_image_stream.ipc".
This module receives the camera images from the Raspberry Pi and transmit them using pynng to the components that need them.

## Software Setup

### Raspberry Pi

Copy the [setup.sh](scripts/setup.sh) to the raspberry pi and run it using:

```bash
sudo chmod +x setup.sh
sudo sh setup.sh
```

It will install all the needed dependencies and create a service to run the camera image stream and DHCP server on boot.

### PC

When the Raspberry Pi is started you will need to wait about half a minute for the DHCP server and Camera Image Stream to start. After waiting the time you can start the receiver script using the [main.py](main.py) script.
