#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='safe',
    version='1.0',
    description='Type-safety utilities for python3',
    author='Ben Longbons',
    author_email='b.r.longbons@gmail.com',
    url='http://github.com/o11c/python-safe',
    packages=[
        'safe',
        'safe.stl',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ]
)
