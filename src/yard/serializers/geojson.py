# from django.core.serializers import serialize
# from yard.consts import RESOURCE_URI_KEYNAME
# from .base import BaseSerializer
# import ujson
#
#
# class GeojsonSerializer(BaseSerializer):
#
#     def to_json(self, resource, is_part_of_collection=True):
#         if not hasattr(resource, '__iter__'):
#             resource = [resource]
#         geojson = serialize('geojson', resource,
#             # geometry_field='point',
#             # fields=[k for k,v in self.fields.iteritems()] + ['pk']
#         )
#         return ujson.loads(geojson)
