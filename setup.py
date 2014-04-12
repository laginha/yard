#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

setup(
    name             = 'yard',
    version          = '2.0.0',
    author           = "Diogo Laginha",
    url              = 'https://github.com/laginha/yard',
    description      = "Yet Another Resftul Django-app",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = ['simplejson', 'rstr', 'django'],
    extras_require   = {},
    zip_safe         = False,
)
