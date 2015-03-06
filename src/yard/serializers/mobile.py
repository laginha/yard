from yard.consts import RESOURCE_PK_KEYNAME
from .base import BaseSerializer


class MobileSerializer(BaseSerializer):
    '''
    Responsible for creating the JSON response optimized for mobile
    '''
    def init_json(self, resource):
        '''
        init JSON for the resource for mobile-driven response 
        '''
        self.links[resource.__class__.__name__] = self.api.get_link( resource )
        return {RESOURCE_PK_KEYNAME: resource.pk}
