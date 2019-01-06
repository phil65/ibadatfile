# -*- coding: utf-8 -*-
"""
@author: Philipp Temminghoff
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ibadatfile",
    version="0.4.0",
    author="Philipp Temminghoff",
    author_email="philipptemminghoff@gmail.com",
    description="Pythonic wrapper for IBA dat file DLL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phil65/ibadatfile/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
)
