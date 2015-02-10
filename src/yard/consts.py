from django.conf import settings

JSON_OBJECTS_KEYNAME = getattr(settings, 'JSON_OBJECTS_KEYNAME', 'Objects')
JSON_META_KEYNAME = getattr(settings, 'JSON_OBJECTS_KEYNAME', 'Meta')
JSON_LINKS_KEYNAME = getattr(settings, 'JSON_LINKS_KEYNAME', 'Meta') 
RESOURCE_URI_KEYNAME = getattr(settings, 'RESOURCE_URI_KEYNAME', 'resource_uri')
RESOURCE_PK_KEYNAME = getattr(settings, 'RESOURCE_PK_KEYNAME', 'pk')
RESOURCE_VERSION_RE = getattr(settings, 'RESOURCE_VERSION_RE', r'.*version=(.*)')
DEFAULT_STATUS_CODE = getattr(settings, 'DEFAULT_STATUS_CODE', 200)