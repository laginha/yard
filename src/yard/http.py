#!/usr/bin/env python
# encoding: utf-8

from django.http import *
import json, mimetypes

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class JsonResponse(HttpResponse):
    def __init__(self, content='', mimetype=None, status=None):
        HttpResponse.__init__(self, content      = json.dumps( content or [], indent=2 ), 
                                    mimetype     = mimetype, 
                                    status       = status, 
                                    content_type = 'application/json', )


class FileResponse(HttpResponse):
    def __init__(self, content='', status=None, content_type=None):
        HttpResponse.__init__(self, content      = content, 
                                    mimetype     = mimetypes.guess_type(content.name)[0], 
                                    status       = status, 
                                    content_type = content_type, )
        self['Content-Disposition'] = 'attachment; filename=' + content.name


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
