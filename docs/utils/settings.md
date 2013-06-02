# Settings

## General

### DEFAULT\_STATUS_CODE

Defines the default status code of the *HTTP* response. Defaults to `200`.

    DEFAULT_STATUS_CODE = 201

### YARD\_DEBUG_MODE

Set this to `True` to enable *Django-Debug-Toolbar* from the JSON responses, if installed and `DEBUG` is `True`. Defaults to `False`. 

    YARD_DEBUG_MODE = True


## Key based authentication

### KEY\_PARAMETER_NAME 

The name of the parameter used for the *API* key. Defaults to `key`.

    KEY_PARAMETER_NAME = "apikey"

### KEY\_AUTH\_401_CONTENT

Message to return in case key based authentication fails.

    KEY_AUTH_401_CONTENT = "You are not authorized"

### KEY\_AUTH\_401_TEMPLATE

Template to render in case key based authentication fails. This setting has priority over `KEY_AUTH_401_CONTENT`. 

    KEY_AUTH_401_TEMPLATE = {
        "template_name": "401.html"
    }
    
The keys to `KEY_AUTH_401_TEMPLATE` are the arguments expected for `django.shortcuts.render`.

### KEY\_EXPIRATION_DELTA

The number of years between the activation date and the expiration date of an *API* key. Defaults to `1`.

    KEY_EXPIRATION_DELTA = 2

### KEY_PATTERN   

The regex pattern of the generated *API* key. Defaults to `r"[a-z0-9A-Z]{30,40}"`

    KEY_PATTERN = r"[a-zA-Z0-9]{10}"

