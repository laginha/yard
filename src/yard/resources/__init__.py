#!/usr/bin/env python
# encoding: utf-8
from .base import BaseResource
from .base.mixins import (
    ElementMixin, CollectionMixin, EditMixin, NewMixin,)
from .base.builders import JSONbuilderForMobile


class CRUDonlyResource(BaseResource, ElementMixin, CollectionMixin):
    pass

class Resource(CRUDonlyResource, EditMixin, NewMixin):
    pass


class CRUDonlyMobileDrivenResource(CRUDonlyResource):
    json_builder_class = JSONbuilderForMobile

class MobileDrivenResource(Resource):
    json_builder_class = JSONbuilderForMobile
