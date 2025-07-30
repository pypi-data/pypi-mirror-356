# -*- coding: utf-8 -*-
from setuptools import setup

import set_pip_mirror

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="set_pip_mirror",
    version=set_pip_mirror.__version__,
    description="set pip mirror to tsinghua",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="sylan215",
    author_email="sylan215@163.com",
    url="https://github.com/sylan215/set_pip_mirror",
    license="MIT License",
    packages=["set_pip_mirror"],
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)
