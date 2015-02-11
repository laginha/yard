from django.conf import settings


DEFAULT_SWAGGER_DESCRIPTION = 'API supported by YARD'
DEFAULT_SWAGGER_TITLE       = 'API documentation'
DEFAULT_SWAGGER_TERMS       = ''
DEFAULT_SWAGGER_CONTACT     = {'email': settings.DEFAULT_FROM_EMAIL}
DEFAULT_SWAGGER_LICENSE     = {
    'name': "Apache 2.0",
    'url': "http://www.apache.org/licenses/LICENSE-2.0.html"
}

SWAGGER_TITLE       = getattr(settings, 'SWAGGER_TITLE', DEFAULT_SWAGGER_TITLE)
SWAGGER_TERMS       = getattr(settings, 'SWAGGER_TERMS', DEFAULT_SWAGGER_TERMS)
SWAGGER_DESCRIPTION = getattr(settings, 'SWAGGER_DESCRIPTION', DEFAULT_SWAGGER_DESCRIPTION)
SWAGGER_CONTACT     = getattr(settings, 'SWAGGER_CONTACT',  DEFAULT_SWAGGER_CONTACT)
SWAGGER_LICENSE     = getattr(settings, 'SWAGGER_LICENSE', DEFAULT_SWAGGER_LICENSE)
    
DEFAULT_SWAGGER_INFO = {
    # 'version': "1.0.0",
    'description':    SWAGGER_DESCRIPTION,
    'title':          SWAGGER_TITLE,
    'termsOfService': SWAGGER_TERMS,
    'contact':        SWAGGER_CONTACT,
    'license':        SWAGGER_LICENSE,
}

SWAGGER_INFO = getattr(settings, 'SWAGGER_INFO', DEFAULT_SWAGGER_INFO)


ALL_SWAGGER_RESPONSES = {
    404: {'description': "Not found"},
    401: {'description': "Not authorized"},
    403: {'description': "Access forbidden"},
    200: {'description': "Successful operation"},
    201: {'description': "Successfully created"},
}
DEFAULT_SWAGGER_RESPONSES = {
    200: ALL_SWAGGER_RESPONSES[200],
}

DEFAULT_SWAGGER_CONTENT_TYPES = [
    "application/json", 
    "application/javascript", 
    "text/html",
]
SWAGGER_CONTENT_TYPES = getattr(settings, 'SWAGGER_CONTENT_TYPES', DEFAULT_SWAGGER_CONTENT_TYPES)


# DEFAULT_SWAGGER_SUPPORTED_METHODS = ['get',]
# DEFAULT_SWAGGER_DOC_EXPANSION = "none"
# DEFAULT_SWAGGER_SORTER = "alpha"
#
# SWAGGER_SUPPORTED_METHODS = getattr(settings, 'SWAGGER_SUPPORTED_METHODS',
#     DEFAULT_SWAGGER_SUPPORTED_METHODS)
# SWAGGER_DOC_EXPANSION = getattr(settings, 'SWAGGER_DOC_EXPANSION',
#     DEFAULT_SWAGGER_DOC_EXPANSION)
# SWAGGER_SORTER = getattr(settings, 'SWAGGER_SORTER',
#     DEFAULT_SWAGGER_SORTER)
#
# DEFAULT_SWAGGER_SETTINGS = {
#     # 'url': url,
#     'dom_id': "swagger-ui-container",
#     'supportedSubmitMethods': SWAGGER_SUPPORTED_METHODS,
#     'docExpansion': SWAGGER_DOC_EXPANSION,
#     'sorter' : DEFAULT_SWAGGER_SORTER
#     # 'highlightSizeThreshold':
# }
#     # 'api_version': '0.1',
#     # 'api_path': '/',
#     # 'api_key': '',
#     # 'is_authenticated': False,
#     # 'is_superuser': False,
#     # 'permission_denied_handler': None,
#
# SWAGGER_SETTINGS = getattr(settings, 'SWAGGER_SETTINGS', DEFAULT_SWAGGER_SETTINGS)
