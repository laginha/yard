# Versioning

One of the most important features related to REST APIs is versioning. When a resource representation is changed in a non-backward compatible way, the resource should be versioned in order to provide any of the representations if requested.


## How To

The example below `BookResourceV2` and `BookResourceV3` are new versions (subclasses) of `BookResource` and each one is expected to be available through versioning.

```python
from yard import resources

class BookResource(resources.Resource):
    fields = ('id', 'title', 'author')
    ...

class BookResourceV2(BookResource):
    fields = ('id', 'title')
    
class BookResourceV3(BookResource):
    index_fields = ('id',)
```    


### ResourceVersions

This class is responsible for resource versioning. Each subclass of `ResourceVersions` requires the `default` attribute. This will be used whenever no version is mentioned in the HTTP request.

```python
from yard import versions

class BookResourceVersions(version.ResourceVersions):
    v1 = BookResource
    v2 = default = BookResourceV2
    v3 = latest  = BookResourceV3
```    

*urls.py*

```python
from yard.api import Api

api = Api()
api.include( 'books', BookResourceVersions )
urlpatterns = api.urlpatterns
```

In this way the `BookResourceVersions` replies to:

- version *v1*, that corresponds to the `BookResource` representation.
- version *v2* and *default*, that corresponds to the `BookResourceV2` representation.
- version *v3* and *latest*, that corresponds to the `BookResourceV3` representation.


### Requesting data

The specific *version* of a resource can be mentioned as a request query input

    http://example.com/books/?version=v1

or it can be stated in the *Accept* header of the request.
