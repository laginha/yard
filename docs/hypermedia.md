# Hypermedia API

*Yard* supports Hypermedia APIs (not in its full extention yet). With this feature APIs are browseable and friendlier to web-crawler and API-clients.

In practice, every returned resource or nested resource contains in its *JSON* representation an *resource_uri* field.

<pre>
{
    "Objects": [
        {
            "id": 18, 
            "author": {
                "id": 10
                "name": "George R.R. Martin", 
                "resource_uri": /authors/10
            }, 
            "title": "A Feast for Crows"
            "resource_uri": /books/18
        }, 
        ...
    ], 
    "Meta": {
        ...
    }
}
</pre>

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
