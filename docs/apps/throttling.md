# Django Throttling

Check out [this project](https://github.com/laginha/django-throttling)!

```python
INSTALLED_APPS = (
    ...
    'throttling',
)
```

```python
from yard.resources import Resource
from yard.decorators.django_throttling import throttle

class Book(Resource):

    class Meta:
        model = models.Book

    @throttle()
    def list(self, request):
        ...
```
