# #!/usr/bin/env python
# # encoding: utf-8
# from django.conf.urls.defaults    import patterns, url, include
# from django.views.decorators.csrf import csrf_exempt
# from yard.version import ResourceVersions
# 
# # allowed http-methods mapped with respective resource-method
# collection = {'get':'index', 'post':'create'}
# single     = {'get':'show', 'put':'update', 'post':'update', 'delete':'destroy'}
# 
# def include_resource(resource, single_name=None, collection_name=None):
#     '''
#     include resource urls for single and collection access
#     '''    
#     urlpatterns = patterns('',
#         # url for resource collection access
#         url( r'^/(?P<pk>[0-9]+)/?$', csrf_exempt(resource(single)), name=single_name ),
#         # url for single resource access
#         url( r'^/?$',                csrf_exempt(resource(collection)), name=collection_name ),
#     )
#     return include( urlpatterns )
