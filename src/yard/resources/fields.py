#!/usr/bin/env python
# encoding: utf-8
import simplejson

Integer = int
Float   = float
List    = Tuple = Iter = list
Dict    = JSON = dict
Unicode = String = unicode
Boolean = bool
GEOJSON        = lambda resource: simplejson.loads(resource.geojson)
RelatedManager = lambda resource: [unicode(i) for i in resource.all()]
QuerySet       = lambda resource: [unicode(i) for i in resource]
ValuesSet      = lambda resource: list( resource )
URI            = lambda resource, api: api.get_uri(resource)
