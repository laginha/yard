#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup, find_packages
from pip.req import parse_requirements

# def parse_requirements():
#     return pip.req.parse_requirements('requirements.txt')
#
# install_requires = [
#     str(each.req) for each in parse_requirements() if each.req
# ]

setup(
    name             = 'yard',
    version          = '2.1a0',
    author           = "Diogo Laginha",
    author_email     = "diogo.laginha.machado@gmail.com",
    url              = 'https://github.com/laginha/yard',
    description      = "Yet Another Resftul Django framework",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = ['Django', 'simplejson', 'rstr', 'gpolyencode'],
    # dependency_links = ,
    extras_require   = {},
    zip_safe         = False,
    license          = 'MIT',
    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Intended Audience :: Developers',
    ]
)
