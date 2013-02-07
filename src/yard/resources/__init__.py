#!/usr/bin/env python
# encoding: utf-8
from django.conf               import settings
from django.core.exceptions    import ObjectDoesNotExist
from django.core.paginator     import Paginator, EmptyPage
from django.core               import serializers
from django.http               import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from yard.exceptions           import RequiredParamMissing, HttpMethodNotAllowed, InvalidStatusCode, MethodNotImplemented
from yard.forms                import Form
from yard.utils                import *
from yard.utils.http           import FileResponse, HttpResponseUnauthorized, JSONResponse, ProperJsonResponse
from yard.resources.parameters import ResourceParameters
from yard.resources.builders   import JSONbuilder
from yard.resources.templates  import ServerErrorTemplate
from yard.resources.meta       import ResourceMeta
from yard.resources.page       import ResourcePage
import json, mimetypes

class CRUDonlyResource(BaseResource, ElementMixin, CollectionMixin):
    pass

class Resource(object):
    '''
    API Resource object
    '''
    
    class Meta(object):
        pass
    
    class Page(object):
        pass

    def __init__(self, routes):
        self.__routes     = routes # maps http methods with respective views
        self.__meta       = ResourceMeta( self.Meta )
        self.__page       = ResourcePage( self.page if hasattr(self, 'page') else self.Page )  
        self.fields       = self.fields if hasattr(self, "fields") else ()
        self.index_fields = self.index_fields if hasattr(self, "index_fields") else self.fields
        self.show_fields  = self.show_fields  if hasattr(self, "show_fields") else self.fields
        self.__parameters = self.parameters() if hasattr(self, "parameters") else (
                                self.Parameters() if hasattr(self, "Parameters") else None )
  
    def __call__(self, request, **parameters):
        '''
        Called in every request made to Resource
        '''
        try:
            method = self.__method( request )
            if method == 'index':
                resource_parameters = self.__resource_parameters( request, parameters )
                builder, current_fields = self.__get_builder(self.index_fields, resource_parameters)
            elif method == 'show':
                resource_parameters = parameters
                builder, current_fields = self.__get_builder(self.show_fields, resource_parameters)
            else:
                resource_parameters = parameters
                builder, current_fields = self.__get_builder(self.fields, resource_parameters)
            response = self.__view( request, method, resource_parameters )
            return self.__response( request, response, current_fields, resource_parameters, builder )   
        except HttpMethodNotAllowed:
            # if http_method not allowed for this resource
            return HttpResponseNotFound()
        except RequiredParamMissing as e:
            # if required param missing from request
            return HttpResponseBadRequest()
        except MethodNotImplemented as e:
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
            return ServerErrorTemplate(e)

class CRUDonlyMobileDrivenResource(CRUDonlyResource):
    json_builder_class = JSONbuilderForMobile

class MobileDrivenResource(Resource):
    json_builder_class = JSONbuilderForMobile
