#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""""

import setuptools

setuptools.setup(
    name="gtjevents",
    version="0.2.0",
    url="https://github.com/ssheftel/gtj-events-scraper.git",

    author="Sam Getz Sheftel",
    author_email="sngsheftel@gmail.com",

    description="scrap events data from gtj",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
