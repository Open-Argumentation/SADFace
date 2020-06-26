#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sadface',
    description='SADFace - The Simple Argument Description Format',
    long_description=readme,
    license=license,
    author='Simon Wells',
    url='https://github.com/ARG-ENU/SADFace.git',
    author_email='mail@simonwells.org',
    version='0.5',
    packages=find_packages(exclude=('deploy', 'etc', 'examples'))
)
