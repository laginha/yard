#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.http import HttpResponse
from yard.utils import is_file, is_int, is_str, is_dict, is_list, is_generator
from yard.utils import is_httpresponse, is_queryset, is_modelinstance, is_valuesset
import simplejson, mimetypes

DEBUG_TOOLBAR_TAG = getattr(settings, 'DEBUG_TOOLBAR_CONFIG', {}).get('TAG', 'body')
DEFAULT_STATUS_CODE = getattr(settings, 'DEFAULT_STATUS_CODE', 200)
IN_DEBUG_MODE = getattr(settings, 'DEBUG', False) and\
                getattr(settings, 'YARD_DEBUG_MODE', False) and\
                'debug_toolbar' in settings.INSTALLED_APPS and\
                hasattr(settings, 'DEBUG_TOOLBAR_CONFIG')


class FileResponse(HttpResponse):
    '''
    Http Response with file content
    '''
    def __init__(self, content='', status=None, filename=None):
        HttpResponse.__init__(self, content      = content, 
                                    content_type = mimetypes.guess_type(content.name)[0], 
                                    status       = status, )
        self['Content-Disposition'] = 'attachment; filename=' + filename or content.name


class JSONResponse(HttpResponse):
    '''
    Http Response with Json content type
    '''
    def __init__(self, content='', status=None):
        content = simplejson.dumps( content, ensure_ascii=False )
        HttpResponse.__init__(self, content      = content, 
                                    status       = status, 
                                    content_type = 'application/json; charset=utf-8', )


class JSONPResponse(HttpResponse):
    '''
    Http Response with Jsonp content type
    '''
    def __init__(self, content='', status=None, callback='callback'):
        content = simplejson.dumps( content, ensure_ascii=False )
        HttpResponse.__init__(self, content      = "%s(%s)" %(callback, content), 
                                    status       = status, 
                                    content_type = 'application/javascript; charset=utf-8', )


class JsonDebugResponse(type):
    '''
    HTTP Response for debug purposes (django-debug-toolbar)
    '''
    def __call__(self, content='', status=None, context=None):
        content = simplejson.dumps( content, ensure_ascii=False )
        return HttpResponse(content = "<%s>%s</%s>" %(DEBUG_TOOLBAR_TAG, content, DEBUG_TOOLBAR_TAG),
                            status  = status, )


class SmartJsonResponse(type):
    '''
    HTTP Response for either JSON or JSONp
    '''
    def __call__(self, content='', status=None, context=None):
        callback = context.GET.get('callback', None) if context else None
        if callback:
            return JSONPResponse(content, status, callback)
        return JSONResponse(content, status)


class JsonResponse(HttpResponse):        
    __metaclass__ = JsonDebugResponse if IN_DEBUG_MODE else SmartJsonResponse


def to_http(request, content=None, status=DEFAULT_STATUS_CODE):
    if is_httpresponse(content):
        return content
    elif content == None:
        return HttpResponse(status=status)
    elif is_int(content):
        return HttpResponse(status=content)
    elif is_str(content) or is_dict(content) or is_list(content):
        return JsonResponse(content, status=status, context=request)
    elif is_file(content):
        return FileResponse(content, status=status)
    elif is_queryset(content):
        return JsonResponse(content.values(), status=status, context=request)
    elif is_modelinstance(content):
        content = [f.name for f in content._meta.fields if f.name not in ['mymodel_ptr']]
        return JsonResponse(content, status=status, context=request)
    elif is_valuesset(content) or is_generator(content):
        return JsonResponse(list(content), status=status, context=request)      
    else:
        return HttpResponse(str(content), status=status)
