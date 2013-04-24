# Settings

## General

### DEFAULT_STATUS_CODE

Defines the default status code of the *HTTP* response. Defaults to `200`.

    DEFAULT_STATUS_CODE = 200


## Key based authentication

### KEY\_PARAMETER_NAME 

The name of the parameter used for the *API* key. Defaults to `key`

### KEY\_AUTHENTICATION_FAIL

Message to return in case key based authentication fails.

### KEY\_EXPIRATION_DELTA

The number of years between the activation date and the expiration date of an *API* key. Defaults to `1`.

### KEY_PATTERN   

The regex pattern of the generated *API* key. Defaults to `r"[a-z0-9A-Z]{30,40}"`
