from django.conf import settings


DEFAULT_SWAGGER_LICENSE = {
    'name': "Apache 2.0",
    'url':  "http://www.apache.org/licenses/LICENSE-2.0.html"
}
DEFAULT_SWAGGER_RESPONSES = {
    404: {'description': "Not found"},
    403: {'description': "Access forbidden"},
    401: {'description': "Not authorized"},
    400: {'description': "Bad request"},
    201: {'description': "Successfully created"},
    200: {'description': "Successful operation"},
}
DEFAULT_SWAGGER_CONTENT_TYPES = [
    "application/json", 
    "application/javascript", 
    "text/html",
]


DEFAULT_SWAGGER_CONTACT = {
    'name':  getattr(settings, 'SWAGGER_CONTACT_NAME',  'API support'),
    'email': getattr(settings, 'SWAGGER_CONTACT_EMAIL', settings.DEFAULT_FROM_EMAIL),
    'url':   getattr(settings, 'SWAGGER_CONTACT_URL',   ''),
} 
DEFAULT_SWAGGER_INFO = {
    'version':        getattr(settings, 'SWAGGER_API_VERSION', '1.0.0'),
    'title':          getattr(settings, 'SWAGGER_TITLE',       'API documentation'),
    'description':    getattr(settings, 'SWAGGER_DESCRIPTION', 'API supported by YARD'),
    'termsOfService': getattr(settings, 'SWAGGER_TERMS',       ''),
    'contact':        getattr(settings, 'SWAGGER_CONTACT',  DEFAULT_SWAGGER_CONTACT),
    'license':        getattr(settings, 'SWAGGER_LICENSE', DEFAULT_SWAGGER_LICENSE),
}


SWAGGER_INFO                   = getattr(settings, 'SWAGGER_INFO',                   DEFAULT_SWAGGER_INFO)
SWAGGER_RESPONSES_DEFINITIONS  = getattr(settings, 'SWAGGER_RESPONSES_DEFINITIONS',  DEFAULT_SWAGGER_RESPONSES)
SWAGGER_CONSUMES               = getattr(settings, 'SWAGGER_CONSUMES',               DEFAULT_SWAGGER_CONTENT_TYPES)
SWAGGER_PRODUCES               = getattr(settings, 'SWAGGER_PRODUCES',               DEFAULT_SWAGGER_CONTENT_TYPES)
SWAGGER_SECURITY_DEFINITIONS   = getattr(settings, 'SWAGGER_SECURITY_DEFINITIONS',   [])
SWAGGER_SECURITY               = getattr(settings, 'SWAGGER_SECURITY',               [])
SWAGGER_TAGS                   = getattr(settings, 'SWAGGER_TAGS',                   [])
SWAGGER_EXTERNAL_DOCS          = getattr(settings, 'SWAGGER_EXTERNAL_DOCS',          {})
SWAGGER_DEFINITIONS            = getattr(settings, 'SWAGGER_DEFINITIONS',            {})
SWAGGER_PARAMETERS_DEFINITIONS = getattr(settings, 'SWAGGER_PARAMETERS_DEFINITIONS', {})


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
