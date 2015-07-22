from django.core.serializers import serialize
from yard.consts import RESOURCE_URI_KEYNAME
from .base import BaseSerializer
import ujson


class GeojsonSerializer(BaseSerializer):
    def to_json(self, resource, is_part_of_collection=True):
        if not is_part_of_collection:
            resource = [resource]        
        geojson = serialize('geojson', resource,
            geometry_field='point',
            fields=self.fields
        )
        return ujson.loads(geojson)
