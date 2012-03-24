#!/usr/bin/env python
# encoding: utf-8

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError, HttpResponseNotFound, HttpResponseBadRequest
import json

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class JsonResponse(HttpResponse):
    def __init__(self, content='', mimetype=None, status=None, content_type=None):
        HttpResponse.__init__(self, content      = json.dumps( content or [], indent=2 ), 
                                    mimetype     = mimetype, 
                                    status       = status, 
                                    content_type = 'application/json', )


def JsonpResponse(req, data):
    #JSONP builder
    json_str = lambda x: json.dumps( x, indent=2 )
    response = HttpResponse( json_str( data ), content_type='application/json' )
    if response.status_code == 200:
        for key in ['callback', 'jsonp']:
            if key in req.GET:
                response['Content-Type'] = 'text/javascript; charset=utf-8'
                response.content = "%s(%s)" %( req.GET[key], response.content )
                return response
    return response
