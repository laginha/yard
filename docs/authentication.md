# Authentication

The authentication module for *Yard* is provided through the `yard.apps.keyauth` application.


## How to

### Settings

Add the following to your settings file:

```python
INSTALLED_APPS = (
    ...
    'yard.apps.keyauth',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'yard.apps.keyauth.backends.KeyAuthBackend',
)
```

If you wish all your views to be protected, you can use the `ApiKeyRequiredMiddleware`.

```python
MIDDLEWARE_CLASSES = (
    ...
    'yard.apps.keyauth.middleware.ApiKeyRequiredMiddleware',
)
```

This middleware must come before the `yard.middleware.SimpleResponseMiddleware`.


### Decorator

To protect a specific view use the `key_required` decorator

```python
from yard import resources
from yard.apps.keyauth.decorators import key_required

class FooResource(resources.Resource):

    @key_required
    def show(self, request, book_id):
        return "bar"
```

When requesting the resource, *yard* looks for the `key` parameter in the *HTTP* request to proceed with the authentication

    http://example.com/foo/1/?key=somegeneratedapikey

You can change the name of the parameter through the `KEY_PARAMETER_NAME` setting.


## Models


### yard.apps.keyauth.models.Key

API key for resource access.

#### Fields

- **user**: Foreign key to *Django's* `User` model.           
- **apikey**: The API key code.          
- **activation_date**: The date of creation of the key.
- **expiration_date**: The date from which the key will expire, thus no longer valid (by default, one year after creation).
- **last_used**: The last time the key was used to access a resource.


### yard.apps.keyauth.models.Consumer

*API* consumer allowed (or not) to use a certain API key. Use this model to restrict the use of any api key. 

#### Fields

- **key**: Foreign key to `Key` model.
- **ip**: The *IP* address of the consumer.
- **allowed**: If the consumer is allowed or not to use the *API* key (defaults to *True*).

The `key` and `ip` fields are unique together.

#### Authorization

If not explicitly allowed or not allowed to use a key, the client is authorized to access the *API* if there is no `Consumer` explicitly allowed to use it.

Otherwise, the client is authorized if the `Consumer` with the used key and the client's *IP* is explicitly allowed, and vice-versa.
