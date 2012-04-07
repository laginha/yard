#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name             = 'yard',
    version          = '0.1.0',
    author           = "Diogo Laginha",
    url              = 'https://github.com/laginha/yard',
    description      = "Yet Another Resftul Django-app",
    packages         = find_packages(where='src'),
    install_requires = [],
    extras_require   = {},
)
