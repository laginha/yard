#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings
from django.core import management
from randomizer  import Randomizer
import unittest

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True)
management.setup_environ(settings)

RANDOM = Randomizer()
