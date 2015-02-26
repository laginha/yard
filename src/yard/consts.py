from django.conf import settings


DEFAULT_JSON_OBJECTS_KEYNAME = 'Objects'
DEFAULT_JSON_META_KEYNAME    = 'Meta'
DEFAULT_JSON_LINKS_KEYNAME   = 'Links'
DEFAULT_RESOURCE_URI_KEYNAME = 'resource_uri'
DEFAULT_RESOURCE_PK_KEYNAME  = 'pk'

DEFAULT_RESOURCE_VERSION_RE = r'.*version=(.*)'


JSON_OBJECTS_KEYNAME = getattr(settings, 'JSON_OBJECTS_KEYNAME', DEFAULT_JSON_OBJECTS_KEYNAME)
JSON_META_KEYNAME    = getattr(settings, 'JSON_OBJECTS_KEYNAME', DEFAULT_JSON_META_KEYNAME)
JSON_LINKS_KEYNAME   = getattr(settings, 'JSON_LINKS_KEYNAME', DEFAULT_JSON_LINKS_KEYNAME) 
RESOURCE_URI_KEYNAME = getattr(settings, 'RESOURCE_URI_KEYNAME', DEFAULT_RESOURCE_URI_KEYNAME)
RESOURCE_PK_KEYNAME  = getattr(settings, 'RESOURCE_PK_KEYNAME', DEFAULT_RESOURCE_PK_KEYNAME)
    
RESOURCE_VERSION_RE = getattr(settings, 'RESOURCE_VERSION_RE', DEFAULT_RESOURCE_VERSION_RE)
    
DEFAULT_STATUS_CODE = getattr(settings, 'DEFAULT_STATUS_CODE', 200)

DEFAULT_METADATA_OPTIONS = {
    'no_meta': False,
    'validated_parameters': True,
    'total_objects': True,
    'paginated_objects': True,
    'next_page': True,
    'previous_page': True,
    'average': None,
    'minimum': None,
    'maximum': None,
    'count': None,
    'custom': {},
}
METADATA_OPTIONS = getattr(settings, 'METADATA_OPTIONS', DEFAULT_METADATA_OPTIONS)


DEFAULT_PAGINATION_OPTIONS = {
    'offset_parameter': 'offset',
    'results_parameter': 'results',
    'results_per_page': 25,
    'limit_per_page': 50,
    'no_pagination': False,
}
PAGINATION_OPTIONS = getattr(settings, 'PAGINATION_OPTIONS', DEFAULT_PAGINATION_OPTIONS)
