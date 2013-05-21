#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.http import HttpResponse
from yard.utils import is_file, is_int, is_str, is_dict, is_list, is_generator
from yard.utils import is_httpresponse, is_queryset, is_modelinstance, is_valuesset
import simplejson, mimetypes

DEFAULT_STATUS_CODE = getattr(settings, 'DEFAULT_STATUS_CODE', 200)


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


class JSONResponse(HttpResponse):
    '''
    Http Response with Json content type
    '''
    def __init__(self, content='', mimetype=None, status=None):
        content = simplejson.dumps( content, ensure_ascii=False )
        HttpResponse.__init__(self, content      = content, 
                                    mimetype     = mimetype, 
                                    status       = status, 
                                    content_type = 'application/json; charset=utf-8', )


class JSONPResponse(HttpResponse):
    '''
    Http Response with Jsonp content type
    '''
    def __init__(self, content='', mimetype=None, status=None, callback='callback'):
        #content = simplejson.dumps( content or [], ensure_ascii=False )
        content = simplejson.dumps( content, ensure_ascii=False )
        HttpResponse.__init__(self, content      = "%s(%s)" %(callback, content), 
                                    mimetype     = mimetype,
                                    status       = status, 
                                    content_type = 'application/javascript; charset=utf-8', )


class _SingletonJsonResponse(type):
    def __call__(self, content='', mimetype=None, status=None, context=None):
        callback = context.GET.get('callback', None) if context else None
        if callback:
            return JSONPResponse(content, mimetype, status, callback)
        return JSONResponse(content, mimetype, status)

class JsonResponse(HttpResponse):        
    __metaclass__ = _SingletonJsonResponse



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
