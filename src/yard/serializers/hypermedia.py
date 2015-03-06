from yard.consts import RESOURCE_URI_KEYNAME
from .base import BaseSerializer


class HypermediaSerializer(BaseSerializer):
    def init_json(self, resource):
        '''
        Add resource_uri for hypermedia
        '''
        return {RESOURCE_URI_KEYNAME: self.api.get_uri(resource)}
