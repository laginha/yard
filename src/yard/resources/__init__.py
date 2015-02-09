#!/usr/bin/env python
# encoding: utf-8
from .base import BaseResource, JsonResource
from .base.mixins import (
    ElementMixin, CollectionMixin, EditMixin, NewMixin, OptionsMixin,)
from .base.builders import JSONbuilderForMobile


class BasicCRUDonlyResource(BaseResource, ElementMixin, CollectionMixin):
    pass
    
class BasicResource(BasicCRUDonlyResource, EditMixin, NewMixin, OptionsMixin):
    pass
    

class CRUDonlyResource(JsonResource, ElementMixin, CollectionMixin):
    pass

class Resource(CRUDonlyResource, EditMixin, NewMixin, OptionsMixin):
    pass


class CRUDonlyMobileDrivenResource(CRUDonlyResource):
    json_builder_class = JSONbuilderForMobile

class MobileDrivenResource(Resource):
    json_builder_class = JSONbuilderForMobile
