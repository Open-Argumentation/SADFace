#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='sadface',
    description='SADFace - The Simple Argument Description Format',
    author='Simon Wells',
    license='GNU GPL3',
    url='https://github.com/ARG-ENU/SADFace.git',
    author_email='mail@simonwells.org',
    version='0.5',
    packages=find_packages(exclude=('deploy', 'etc', 'examples'))
)
