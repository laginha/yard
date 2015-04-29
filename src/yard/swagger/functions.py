from yard.consts import RESOURCE_VERSION_RE
from yard.fields import JsonField
from .consts import (
    SWAGGER_CONSUMES, SWAGGER_PRODUCES, SWAGGER_RESPONSES_DEFINITIONS, 
    SWAGGER_SECURITY_DEFINITIONS, SWAGGER_SECURITY, SWAGGER_TAGS,
    SWAGGER_EXTERNAL_DOCS, SWAGGER_DEFINITIONS, 
    SWAGGER_PARAMETERS_DEFINITIONS, SWAGGER_INFO)
import re


def build_swagger_parameter(preset=None, location='', name='', typename='',
                            required=True, description='', **kwargs):
    if preset == 'path':
        return {
            'in'         : 'path', 
            'name'       : 'pk', 
            'type'       : 'integer',
            'required'   : True, 
            'description': 'Resource identification',
        }
    elif preset == 'http_accept':
        return {
            'in'         : 'header', 
            'name'       : 'Accept', 
            'type'       : 'string',
            'required'   : False,
            'description': 'Version identification of the resource',
            'pattern'    : RESOURCE_VERSION_RE,
            'default'    : kwargs.get('default', None), 
        }
    else:
        parameter = {
            'in'      : location, 
            'name'    : name,
            'type'    : typename, 
            'required': required,
        }
        allowed_kwargs = [
            'description', 'default', 'items', 'maximum', 'minimum', 'pattern'
        ]
        for each in allowed_kwargs:
            if kwargs.get(each, None):
                parameter[each] = kwargs[each]
        return parameter
          

def build_swagger_object(request, paths):
    
    def find(keyname, json):
        for key, value in json.items():
            if key == keyname:
                yield json.pop(key)
            elif isinstance(value, dict):
                for result in find(keyname, value):
                    yield result
            elif isinstance(value, list):
                for each in value:
                    if isinstance(each, dict):
                        for result in find(keyname, each):
                            yield result
    
    scheme = request.scheme if hasattr(request, 'scheme') else 'http' 
    result = {
        'swagger':  "2.0",
        'info':     SWAGGER_INFO,
        'host':     request.get_host(),
        'basePath': request.path,
        'schemes':  [scheme],
        'paths':    paths
    }
    if SWAGGER_CONSUMES:
        result['consumes'] = SWAGGER_CONSUMES
    if SWAGGER_PRODUCES:
        result['produces'] = SWAGGER_PRODUCES
    if SWAGGER_RESPONSES_DEFINITIONS:
        result['responses'] = SWAGGER_RESPONSES_DEFINITIONS
    if SWAGGER_SECURITY_DEFINITIONS:
        result['securityDifinitions'] = SWAGGER_SECURITY_DEFINITIONS
    if SWAGGER_SECURITY:
        result['security'] = SWAGGER_SECURITY
    if SWAGGER_TAGS:
        result['tags'] = SWAGGER_TAGS
    if SWAGGER_EXTERNAL_DOCS:
        result['externalDocs'] = SWAGGER_EXTERNAL_DOCS 
    
    schema_definitions = find('schema_definition', paths)
    if SWAGGER_DEFINITIONS:
        result['definitions'] = SWAGGER_DEFINITIONS
    elif schema_definitions:
        result['definitions'] = {}
    for each in schema_definitions:
        result['definitions'].update( each )
        
    if SWAGGER_PARAMETERS_DEFINITIONS:
        result['parameters'] = SWAGGER_PARAMETERS_DEFINITIONS
    return result


def build_swagger_schema(fields):
    result = {}
    for name,fieldtype in fields.iteritems():
        if isinstance(fieldtype, dict):
            result[name] = build_swagger_schema(fieldtype)
        if isinstance(fieldtype, JsonField):
            result[name] = fieldtype.get_documentation()
        elif isinstance(fieldtype, list):
            result[name] = {'type': 'array', 'items': {'type':'string'}}
        elif isinstance(fieldtype, bool):
            result[name] = {'type': 'boolean'}
        elif isinstance(fieldtype, int):
            result[name] = {'type': 'number'}
        elif isinstance(fieldtype, float):
            result[name] = {'type': 'number'}
        else:
            result[name] = {'type': 'string'}
    return {'properties': result}
    
    
def build_swagger_operation(http_method, verb, tagname, 
                            parameters=None, responses=None, **kwargs):
    
    def get_summary():
        if re.match(r'^a|e|i|o|u', tagname):
            return '%s an %s'
        return '%s a %s'
    
    capital_tag = tagname.capitalize()
    result = {
        'tags':        ["%s operations"%capital_tag],
        'summary':     get_summary() %(verb.capitalize(), tagname),
        'operationId': '%s%s' %(verb, capital_tag),
    }
    if parameters:
        result['parameters'] = parameters
    if responses:
        result['responses'] = responses
    result['produces'] = [
        'application/json', 
        'application/javascript',
    ]
    for key,value in kwargs.iteritems():
        result[ key ] = value
    return {http_method.lower(): result}
