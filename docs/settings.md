# Settings

## General

### DEFAULT\_STATUS_CODE

Defines the default status code of the *HTTP* response. Defaults to `200`.

### RESOURCE_VERSION\_RE

Regular expression for fetching the version name/number on the `Accept` request header. 
Defaults to `r'.*version=(.*)'`

### JSON_OBJECTS\_KEYNAME

Defaults to `"Objects"`.

### JSON_METADATA\_KEYNAME

Defaults to `"Meta"`.

### JSON_LINKS\_KEYNAME

Defaults to `"Links"`

### RESOURCE_URI\_KEYNAME

Defaults to `"resource_uri"`

### RESOURCE_PK\_KEYNAME

Defaults to `"pk"`


## Swagger documentation


### SWAGGER_CONTACT\_NAME

Defaults to `'API support'`.

### SWAGGER_CONTACT\_EMAIL   

Defaults to `settings.DEFAULT_FROM_EMAIL`.

### SWAGGER_CONTACT\_URL

Defaults to `""`.

### SWAGGER_API\_VERSION

Defaults to `'1.0.0'`.

### SWAGGER_TITLE

Defaults to `'API documentation'`.

### SWAGGER_DESCRIPTION

Defaults to `'API supported by YARD'`.

### SWAGGER_TERMS

Defaults to `""`.

### SWAGGER_CONTACT

Defaults to:

```python
{
    'name': settings.SWAGGER_CONTACT_NAME,
    'email': settings.SWAGGER_CONTACT_EMAIL,
    'url': settings.SWAGGER_CONTACT_URL,
}
```

### SWAGGER_LICENSE

Defaults to:

```python
{
    'name': "Apache 2.0",
    'url':  "http://www.apache.org/licenses/LICENSE-2.0.html"
}
```

### SWAGGER_INFO   

Defaults to:

```python
{
    'version': settings.SWAGGER_API_VERSION,
    'title': settings.SWAGGER_TITLE,
    'description': settings.SWAGGER_DESCRIPTION,
    'termsOfService': settings.SWAGGER_TERMS,
    'contact': settings.SWAGGER_CONTACT,
    'license': settings.SWAGGER_LICENSE,
}
```
   
### SWAGGER_RESPONSES\_DEFINITIONS 

Defaults to:

```python
{
    404: {'description': "Not found"},
    403: {'description': "Access forbidden"},
    401: {'description': "Not authorized"},
    400: {'description': "Bad request"},
    201: {'description': "Successfully created"},
    200: {'description': "Successful operation"},
}
```

### SWAGGER_CONSUMES

Defaults to:

```python
[
    "application/json", 
    "application/javascript", 
    "text/html",
]
```

### SWAGGER_PRODUCES

Defaults to:

```python
[
    "application/json", 
    "application/javascript", 
    "text/html",
]
```

### SWAGGER_SECURITY\_DEFINITIONS

Defaults to `[]`.

### SWAGGER_SECURITY

Defaults to `[]`.

### SWAGGER_TAGS

Defaults to `[]`.
  
### SWAGGER_EXTERNAL\_DOCS

Defaults to `{}`.

### SWAGGER_DEFINITIONS

Defaults to `{}`.

### SWAGGER_PARAMETERS\_DEFINITIONS

Defaults to `{}`.

### SWAGGER_SUPPORTED\_METHODS

Defaults to `['get', 'post', 'put', 'delete']`.

### SWAGGER_DOC\_EXPANSION    

Defaults to `"list"`.

### SWAGGER_SORTER 

Defaults to `"alpha"`.
    
### SWAGGER_API\_KEY\_NAME 

Defaults to `"key"`.

### SWAGGER_DEFAULT_KEY

Defaults to `""`.

  