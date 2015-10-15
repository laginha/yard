#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup
from setuptools import find_packages

setup(
    name             = 'yard-framework',
    version          = '3.6.0',
    author           = "Diogo Laginha",
    author_email     = "diogo.laginha.machado@gmail.com",
    url              = 'https://github.com/laginha/yard/tree/develop',
    description      = "Yet Another Resftul Django framework",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
    install_requires = [
        'Django',
        'ujson',
        'rstr',
        'gpolyencode',
        'django-easy-response',
        'django-key-auth',
        'django-alo-forms',
        'throttling',
    ],
    extras_require   = {},
    zip_safe         = False,
    license          = 'MIT',
    classifiers      = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Intended Audience :: Developers',
    ]
)
