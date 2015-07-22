# Serializers


## BaseSerializer

This serializer is the foundations of all other serializers. In practice, it serializes the objects to JSON according to the `Resource.Meta.fields` (alternatively, `detail_fields` or `list_fields`) 

```python 
from yard import resources, fields, serializers

class Book(resources.Resource):
    class Meta:
        model = models.Book
        serializer = serializers.BaseSerializer
        fields = {
            'title': fields.Unicode, 
            'author': {
                "name": fields.Unicode,
            }
        }
```

```javascript
{
    "Objects": [
        {
            "author": {
                "name": "George R.R. Martin", 
            },
            "title": "A Feast for Crows",
        }, 
        ...
    ], 
    "Meta": {
        ...
    }
}
```

## HypermediaSerializer

**This is the default serializer**. The only difference to `BaseSerializer` is that it includes a `resource_uri` key to each object and nested object serialized.

```javascript
{
    "Objects": [
        {
            "author": {
                "name": "George R.R. Martin",
                "resource_uri": "/authors/1"
            }, 
            "title": "A Feast for Crows",
            "resource_uri": "/books/1"
        }, 
        ...
    ], 
    "Meta": {
        ...
    }
}

This way API endpoints are browsable and friendlier to API-clients. But for this to work properly both resources, books and authors, must exist in the `Api`.

```python
from yard.api import Api

api = Api()
api.include( r'books', BooksResource )
api.include( r'authors', AuthorsResource)
```

## MobileSerializer

This mobile driven serializer makes the JSON representation lighter without loosing its hypermedia touch. Instead of including and repeating the same `resource_uri`s for each returned object and nested object, as the `HypermediaSerializer` does, it adds only the corresponding `pk` and aggregates all the URIs separately:


```python 
from yard import resources, serializers

class Book(resources.Resource):
    class Meta:
        serializer = serializers.MobileSerializer
        model = models.Book
        ...
```

```javascript
{
    "Objects": [
        {
            "author": {
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

## GeojsonSerializer

Fully compactible GeoJson response schema.

