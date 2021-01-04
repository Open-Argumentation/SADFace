#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md', "r", encoding="utf-8") as f:
    long_description = f.read()

exec(open('sadface/version.py').read())

setup(
    name='sadface',
    description='SADFace - The Simple Argument Description Format',
	long_description_content_type='text/markdown',
    long_description=long_description,
    author='Simon Wells',
    url='https://github.com/Open-Argumentation/SADFace.git',
    author_email='mail@simonwells.org',
	version=__version__,
    packages=find_packages(exclude=('deploy', 'etc', 'examples')),
)
