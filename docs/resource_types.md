# Resource Types


## Resource

This is the main class. Every other *resource type* is a subclass of `Resource`.


## MobileDrivenResource

In comparison to `Resource`, the `MobileDrivenResource` differs in its *hypermedia* implementation. In fact the normal `Resource` *JSON* response, although more readable, is not optimized in its size or length.

```javascript
{
    "Objects": [
        {
            "author": {
                "name": "George R.R. Martin",
                "resource_uri": "path/to/authors/1" 
            }, 
            "title": "A Feast for Crows"
            "resource_uri": "path/to/books/1"
        }, 
        ...
    ], 
    "Meta": {
        ...
    }
}
```

However, the response in a `MobileDrivenResource` is lighter, thus more appropriate for clients with low internet connections, like mobile phones.

```javascript
{
    "Objects": [
        {
            "author": {
                "name": "George R.R. Martin",
                "pk": 1, 
            }, 
            "title": "A Feast for Crows"
            "pk": 1,
        }, 
        ...
    ], 
    "Links": {
        Book: "path/to/books/%s",
        Author: "path/to/authors/%s",
    },
    "Meta": {
        ...
    }
}
```

For this kind of `Resource` it's recommended to use `fields.Link` for consistency, rather than `fields.URI`.

```python
from yard import resources, fields

class FooResource(resources.MobileDrivenResource):
    fields = {
        'title': fields.Unicode,
        'author': fields.Link,
    }
    
    def index(self, request, params):
        return Book.objects.filter(**params)
```
