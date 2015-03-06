# Uglification

You can add extra layer to the JSON response construction (besides [pagination](pagination.md), [serialization](serializers.md) and [metadata inclusion](metadata.md)) through uglification. 

```python 
from yard import resources, fields, serializers

class Book(resources.Resource):
    class Meta:
        model = models.Book
        uglify = True
```

This process may be used whatever is the chosen serializer. It acts upon the resulting JSON, uglifying it and making it lighter.


## Examples

#### HypermediaSerializer

Normal response:

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

Uglified response:

```javascript
{
    "Objects": [
        {
            "a": {
                "b": "George R.R. Martin",
                "c": "path/to/authors/1" 
            }, 
            "d": "A Feast for Crows"
            "c": "path/to/books/1"
        }, 
        ...
    ],
    "Mapping":{
        "a": "author",
        "b": "name",
        "c": "resource_uri",
        "d": "title",
    }, 
    "Meta": {
        ...
    }
}
```


#### MobileSerializer

Normal response:

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

Uglified response:

```javascript
{
    "Objects": [
        {
            "a": {
                "b": "George R.R. Martin",
                "c": 1, 
            }, 
            "d": "A Feast for Crows"
            "c": 1,
        }, 
        ...
    ],
    "Mapping": {
        "a": "author",
        "b": "name",
        "c": "pk",
        "d": "title",
    }, 
    "Links": {
        Book: "path/to/books/%s",
        Author: "path/to/authors/%s",
    },
    "Meta": {
        ...
    }
}
```
