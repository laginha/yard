#!/usr/bin/env python
# encoding: utf-8
from yard.resources.resource import Resource
from yard.resources.utils.builders import JSONbuilderForMobile

class MobileDrivenResource(Resource):
    json_builder_class = JSONbuilderForMobile
