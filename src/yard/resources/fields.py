#!/usr/bin/env python
# encoding: utf-8
import simplejson

Integer = int
Float   = float
List    = Tuple = Iter = list
Dict    = JSON = dict
Unicode = String = unicode
Boolean = bool
GEOJSON        = lambda x: simplejson.loads(x.geojson)
RelatedManager = lambda x: [unicode(i) for i in x.all()]
QuerySet       = lambda x: [unicode(i) for i in x]
ValuesSet      = lambda x: list( result )
URI            = lambda x, api: api.get_uri(x)
