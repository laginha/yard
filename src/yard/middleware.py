#!/usr/bin/env python
# encoding: utf-8
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from yard.utils.http import FileResponse, JSONResponse, ProperJsonResponse
from yard.exceptions import RequiredParamMissing, HttpMethodNotAllowed, InvalidStatusCode, MethodNotImplemented
from yard.utils import is_tuple, is_int, is_httpresponse, is_str, is_dict, is_file

DEFAULT_STATUS = getattr(settings, 'DEFAULT_STATUS', 200)


class YardMiddleware(object):
    
    def run_view(self, request, view, args, kwargs):
        try:
            return view(request, *args, **kwargs)
        except HttpMethodNotAllowed:
            # if http_method not allowed for this resource
            return HttpResponseNotFound()
        except RequiredParamMissing:
            # if required param missing from request
            return HttpResponseBadRequest()
        except MethodNotImplemented:
            # if view not implemented
            return HttpResponseNotFound()
        except ObjectDoesNotExist:
            # if return model instance does not exist
            return HttpResponseNotFound()
        except IOError:
            # if return file not found
            return HttpResponseNotFound()
        except InvalidStatusCode as e:
            # status code given is not int
            return HttpResponse(str(e))
    
    def process_view(self, request, view, args, kwargs):
        response = self.run_view(request, view, args, kwargs)
        status = DEFAULT_STATUS
        
        if is_httpresponse(response):
            return response
        if is_tuple(response) and len(response)>1:
            if is_int( response[0] ):
                status = response[0]
            else:
                raise InvalidStatusCode(response[0])
            response = response[1]
        
        if response == None:
            return HttpResponse(status=status)
        elif is_int(response):
            return HttpResponse(status=response)
        elif is_str(response) or is_dict(response):
            if JSONResponse==ProperJsonResponse:
                return JSONResponse(request)(response, status=status)
            return JSONResponse(response, status=status)
        elif is_file(response):
            return FileResponse(response, status=status)
        else:
            return HttpResponse(str(response), status=status)
    
    