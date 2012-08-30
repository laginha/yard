#!/usr/bin/env python
# encoding: utf-8

from django.http import HttpResponse
import simplejson, mimetypes

class HttpResponseUnauthorized(HttpResponse):
    '''
    Http Response for status 401
    '''
    status_code = 401


class FileResponse(HttpResponse):
    '''
    Http Response with file content
    '''
    def __init__(self, content='', status=None, content_type=None):
        HttpResponse.__init__(self, content      = content, 
                                    mimetype     = mimetypes.guess_type(content.name)[0], 
                                    status       = status, 
                                    content_type = content_type, )
        self['Content-Disposition'] = 'attachment; filename=' + content.name


class JsonResponse(HttpResponse):
    '''
    Http Response with Json content type
    '''
    def __init__(self, content='', mimetype=None, status=None):
        content = simplejson.dumps( content or [], indent=2, ensure_ascii=False )
        HttpResponse.__init__(self, content      = content, 
                                    mimetype     = mimetype, 
                                    status       = status, 
                                    content_type = 'application/json; charset=utf-8', )


class JsonpResponse(HttpResponse):
    '''
    Http Response with Jsonp content type
    '''
    def __init__(self, content='', mimetype=None, status=None, param='callback'):
        content = json.dumps( content or [], indent=2 )
        HttpResponse.__init__(self, content      = "%s(%s)" %(param, content), 
                                    mimetype     = mimetype,
                                    status       = status, 
                                    content_type = 'text/javascript; charset=utf-8', )


class ProperJsonResponse:
    '''
    Json or Jsonp Response according to request
    '''    
    def __init__(self, request):
        self.__jsonp_param = None
        for param in ['callback', 'jsonp']:
            if param in request.GET:
                self.__jsonp_param = param
                
    def __call__(self, *args, **kwargs):
        if self.__jsonp_param:
            return JsonpResponse(*args, param=self.__jsonp_param, **kwargs) 
        return JsonResponse(*args, **kwargs)


import settings
TAG = 'body'
if hasattr(settings, 'DEBUG_TOOLBAR_CONFIG'):
    if 'TAG' in settings.DEBUG_TOOLBAR_CONFIG:
        TAG = settings.DEBUG_TOOLBAR_CONFIG['TAG']


class JsonDebugResponse(HttpResponse):
    '''
    HTTP Response for debug purposes (django-debug-toolbar)
    '''
    def __init__(self, content='', mimetype=None, content_type=None, status=None):
        content = simplejson.dumps( content or [], indent=2, ensure_ascii=False )
        HttpResponse.__init__(self, content      = self.__json_to_html(content),
                                    mimetype     = mimetype,
                                    status       = status, 
                                    content_type = content_type,)
                                    
    def __json_to_html(self, content):
        content = content.replace('\n', '<br/>')
        content = content.replace('  ','&nbsp;&nbsp;&nbsp;&nbsp;')
        if TAG != 'body':
            return "<body><%s>%s</%s></body>" %(TAG, content, TAG)
        return "<%s>%s</%s>" %(TAG, content, TAG)


    
    
    
