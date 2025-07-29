#!/usr/bin/env python
"""Setup."""

import importlib

from setuptools import setup, find_packages

# read the contents of the README file
with open("README.md", encoding="utf-8") as f:
    README = f.read()

VERSION = "0.0.4"


setup(
    name="dataframe-pointer",
    author="Hugo Dictus",
    author_email="h.t.dictus@gmail.com",
    version=VERSION,
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    license="GNU GPL",
    install_requires=[
        'pandas'
    ],
    packages=find_packages(),
    python_requires=">=3.6"
)
