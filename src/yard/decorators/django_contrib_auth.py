#!/usr/bin/env python
# encoding: utf-8
from django.contrib.auth.decorators import permission_required as original_permission_required
from django.contrib.auth.decorators import login_required as original_login_required
from .utils import to_yard_decorator

@to_yard_decorator
def login_required(): 
    return original_login_required

@to_yard_decorator
def permission_required():
    return original_permission_required
