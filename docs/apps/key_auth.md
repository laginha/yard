# Django Key Auth

Check out [this project](https://github.com/laginha/django-key-auth)!

```python
INSTALLED_APPS = (
    ...
    'keyauth',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'keyauth.backends.KeyAuthBackend',
)

MIDDLEWARE_CLASSES = (
    ...
    'keyauth.middleware.KeyAuthenticationMiddleware',
)
```

```python
from yard.resources import Resource
from yard.decorators import key_required

class Book(Resource):

    class Meta:
        model = models.Book

    @key_required()
    def list(self, request):
        key = request.key
        ...
```
