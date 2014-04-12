# Uglification

As discussed in [here](resource_types.md), using `MobileDrivenResource` results in a lighter *JSON* response. However you can also uglify *JSON* responses to optimize the response, whatever the resource type.

## Resource

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


## MobileDrivenResource

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
