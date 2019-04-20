#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

setup(
    name='SADFace',
    description='SADFace - The Simple Argument Description Format',
    author='Simon Wells',
    license='GNU GPL3',
    url='https://github.com/ARG-ENU/SADFace.git',
    author_email='mail@simonwells.org',
    version='0.2',
    install_requires=['requests'],
)
