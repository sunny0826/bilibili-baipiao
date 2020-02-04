#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
from sys import version_info

from setuptools import setup, find_packages

if version_info[:2] < (3, 5):
    raise RuntimeError(
        'Unsupported python version %s.' % '.'.join(version_info)
    )

_NAME = 'baipiao'

setup(
    name=_NAME,
    version='0.0.1',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    author='Guoxudong',
    author_email='sunnydog0826@gmail.com',
    include_package_data=True,
    install_requires=[
        'requests',
        'tqdm',
        'pyfiglet',
        'prettytable',
    ],
    entry_points={
        'console_scripts': [
            '{0} = bilibili.main:main'.format(_NAME),
        ]
    }
)
