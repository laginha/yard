# Versioning

One of the most important features related to REST APIs is versioning. When a resource representation is changed in a non-backward compatible way, the resource should be versioned in order to provide any of the representations if requested.

> Resource versioning is taken into consideration by the [API documentation module](meta/documentation.md).


## How To

The example below `BookResourceV2` and `BookResourceV3` are new versions (subclasses) of `BookResource` and each one is expected to be available through versioning.

```python
from yard import resources

class BookResource(resources.Resource):
    class Meta:
        model = models.Book
    
    def list(self, request):
        return models.Book.objects.all()

class BookResourceV2(BookResource):
    class Meta:
        model = models.Book
        fields = {
            'title': fields.Unicode, 
            'author': fields.Unicode
        }
    
class BookResourceV3(BookResource):
    class Meta:
        model = models.Book
        fields = {
            'title': fields.Unicode, 
        }
```    


### VersionController

This class is responsible for resource versioning. Each subclass of `VersionController` requires the `default` attribute. This will be used whenever no version is mentioned in the HTTP request.

```python
from yard.version import VersionController

class BookVersionController(VersionController):
    versions = {
        '1.0': BookResource,
        '2.0': BookResourceV2,
        '3.0': BookResourceV3,
    }
    default = '2.0'
    latest  = '3.0'
```    

```python
from yard.api import Api

api = Api()
api.include( 'books', BookVersionController )
urlpatterns = api.urlpatterns
```

In this way the `BookResourceVersions` replies to:

- version *1.0*, that corresponds to the `BookResource` representation.
- version *2.0* and *default*, that corresponds to the `BookResourceV2` representation.
- version *3.0* and *latest*, that corresponds to the `BookResourceV3` representation.


### Requesting data

The specific *version* of a resource can be mentioned as a request query input

    http://example.com/books/?version=1.0

or it can be stated in the *Accept* header of the request

    ACCEPT: version=1.0

    ACCEPT: application/json; version=1.0
