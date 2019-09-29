#!/usr/bin/env python3

"""Setup script."""

from setuptools import setup

setup(
    name="greetings",
    version="0.0.0",
    author="Arthur Khashaev",
    author_email="arthur@khashaev.ru",
    url="https://github.com/PPPoSD-2017/greetings",
    license="MIT",
    setup_requires=[
        "colorama",
        "pycodestyle",
    ],
    tests_require=[
        "colorama",
        "pycodestyle",
    ]
)
