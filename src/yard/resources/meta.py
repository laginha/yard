from yard.swagger import Documentation
from yard.metadata import Metadata
from yard.pagination import Pagination
from yard.serializers import HypermediaSerializer
from yard.exceptions import NoModelError
from yard.fields import get_field as get_json_field
import copy


def model_to_fields(model):
    fields = model._meta.fields
    return dict([
        (each.name, get_json_field(each)) for each in fields
    ])


class ResourceMeta(object):
    
    DEFAULTS = {
        'model': None,
        'serializer': HypermediaSerializer,
        'uglify': False,
        'documentation': Documentation,
        'metadata': Metadata,
        'pagination': Pagination,
    }
    
    def __init__(self, resource):
        
        def get_meta_attribute(name):
            return getattr(resource.Meta, name, self.DEFAULTS.get(name))
        
        self.model = get_meta_attribute('model')
        if not self.model:
            raise NoModelError
        self.documentation = get_meta_attribute('documentation')(resource)
        self.pagination    = get_meta_attribute('pagination')()
        self.metadata      = get_meta_attribute('metadata')(self.pagination)
        self.uglify        = get_meta_attribute('uglify')
        self.serializer    = get_meta_attribute('serializer')
        
        def get_fields(name, default=None):
            if hasattr(resource.Meta, name):
                return copy.deepcopy(getattr(resource.Meta, name))
            return model_to_fields(self.model) if not default else default
        
        self.fields        = get_fields('fields')
        self.detail_fields = get_fields('detail_fields', self.fields)
        self.list_fields   = get_fields('list_fields', self.fields)
