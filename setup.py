#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup, find_packages
import pip

def parse_requirements():
    return pip.req.parse_requirements('requirements.txt')
    
install_requires = [
    str(each.req) for each in parse_requirements() if each.req
]

setup(
    name             = 'yard',
    version          = '2.1a0',
    author           = "Diogo Laginha",
    url              = 'https://github.com/laginha/yard',
    description      = "Yet Another Resftul Django-app",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = install_requires,
    # dependency_links = ,
    extras_require   = {},
    zip_safe         = False,
)
