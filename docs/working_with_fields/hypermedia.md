# Hypermedia API

*Yard* supports Hypermedia APIs (not in its full extension yet). With this feature APIs are browsable and friendlier to API-clients.

In practice, if using `Resource`, every returned resource or nested resource contains in its *JSON* representation an *resource_uri* field.

```javascript
{
    "Objects": [
        {
            "author": {
                "id": 10
                "name": "George R.R. Martin", 
                "resource_uri": "/authors/10"
            }, 
            "title": "A Feast for Crows"
            "resource_uri": "/books/18"
        }, 
        ...
    ], 
    "Meta": {
        ...
    }
}
```

However, if using `MobileDrivenResource`, the *JSON* response is different but lighter and faster

```javascript
{
    "Objects": [
        {
            "author": {
                "id": 10
                "name": "George R.R. Martin", 
                "pk": 10
            }, 
            "title": "A Feast for Crows"
            "pk": 18
        }, 
        ...
    ], 
    "Links": {
        "Book": "/books/%s",
        "Author": "/authors/%s"
    },
    "Meta": {
        ...
    }
}
```

For this to work properly both resources, books and authors, must exist in the `Api`.

```python
from yard.api import Api

api = Api()
api.include( r'books', BooksResource )
api.include( r'authors', AuthorsResource)
```

and at least the `AuthorsResource` (because `author` is referenced by `book`) must have the `model` attribute defined.

```python  
from yard import resources

class AuthorsResource(resources.Resource):    
    model = Author
```
