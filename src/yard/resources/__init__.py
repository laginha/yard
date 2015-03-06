#!/usr/bin/env python
# encoding: utf-8
from .base import BaseResource
from .mixins import ElementMixin, CollectionMixin, EditMixin, NewMixin
from yard.serializers import MobileSerializer


class Resource(BaseResource, ElementMixin, CollectionMixin, EditMixin, NewMixin):
    pass
