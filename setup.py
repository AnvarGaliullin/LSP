#!/usr/bin/env python3

"""Setup script."""

from setuptools import setup

setup(
    name="Hangman",
    version="1.0.0",
    author="Anvar Galiullin",
    author_email="anvargal@mail.ru",
    url="https://github.com/AnvarGaliullin/HangMan-Game",
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
