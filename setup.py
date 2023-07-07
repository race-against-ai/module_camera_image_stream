# Copyright (C) 2023, NG:ITL
import versioneer
from pathlib import Path
from setuptools import find_packages, setup


def read(fname):
    return open(Path(__file__).parent / fname).read()


setup(
    name="raai_module_camera_image_stream",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="NGITl",
    author_email="666arnehilbig@gmail.com",
    description=("RAAI Module Camera Image Stream for recieving the camera images from the Raspberry Pi."),
    license="GPL 3.0",
    keywords="camera image stream",
    url="https://github.com/vw-wob-it-edu-ngitl/raai_module_camera_image_stream",
    packages=find_packages(),
    long_description=read("README.md"),
    install_requires=["pynng~=0.7.2", "numpy~=1.24.2", "opencv-python~=4.7.0.72"],
)
