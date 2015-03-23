# List of types

Choosing the *field type* is not only a matter of semantics. It influences the *JSON* response structure, as well as, the number of queries to the database.

### Integer

Return JSON field as an integer.

```python
fields = {
    'id': fields.Integer
}
```

### Float

Return JSON field as a float.

```python
fields = {
    'id': fields.Float
}
```
### List
    
Return JSON field as a list.

```python
fields = {
    'authors': fields.List
}    
```

### Dict

Return JSON field as a dictionary.

```python
fields = {
    'extradata': fields.dict
}
```

### JSON

Alias for ´fields.dict´

### String
   
Return JSON field as a sring.

```python
fields = {
    'name': fields.String
}
``` 
 
### Unicode

Return JSON field as an unicode.

```python
fields = {
    'name': fields.Unicode
}
```

### ForeignKey
   
Same as `Unicode` although it enables *Yard* to automatically optimize the database query using `QuerySet.select_related`.

```python
fields = {
    'author': fields.ForeignKey
}
```

### GenericForeignKey
   
Same as `Unicode` although it enables *Yard* to automatically optimize the database query using `QuerySet.prefetch_related`.

```python
fields = {
    'genres': fields.GenericForeignKey
}
```
   
### Boolean

Return JSON field as a boolean.

```python
fields = {
    'is_male': fields.Boolean
}
```
       
### CommaSeparatedValue

Return JSON field as a comma separated value.

```python
fields = {
    'authors': fields.CommaSeparatedValue
}
```

### File

Return JSON field as an URL for the file.

```python
fields = {
    'image': fields.File
}
```

### FilePath

Return JSON field as an file path.

```python
fields = {
    'image': fields.FilePath
}
```

### RelatedManager

Return JSON field as a list of unicode values for RelatedManager input.

```python
fields = {
    'genres': fields.RelatedManager
}
```

### QuerySet

Return JSON field as a list of unicode values for QuerySet input.

```python
fields = {
    'authors': fields.QuerySet
}
```

### ValuesSet

Return JSON field as a list for ValuesSet input.

```python
fields = {
    'authors': fields.ValuesSet
}
```

### URI

Return JSON field as an URI.

```python
fields = {
    'author': fields.URI
}
```    
    
This type expects a *model instance* as input which `Model` class is referenced by a `Resource`.

```python
from yard import resources, fields

class AuthorsResource(resources.Resource):    
    model = Author
    fields = {
        'id': fields.URI
    }
    
    def index(self, request, params):
        return Author.objects.all(**params)
        
    def show(self, request, object_id):
        return Author.objects.get(pk=object_id)
```

### Link

Return the `pk` as JSON field value and adds *incomplete-URI* to *JSON* response field *Links*. 

Just like `fields.URI`, this type expects a *model instance* as input which `Model` class is referenced by a `Resource`.

```python
fields = {
    'author': fields.Link
}
```

```javascript
{
    "Objects": [
        {
            "author": 1
        }, 
        ...
    ], 
    "Links": {
        "author": "path/to/author/%s",
    }
}
```

This is an lighter alternative to the `field.URI`! See the also the documentation about [MobileDrivenResource](resource_types.md).


### Auto

Return JSON field with the type most appropriated for the input.

```python
fields = {
    'id': fields.Auto
}
```

If you are too lazy to specify the field type, this is a good solution for you. However this won't work properly for certain class objects like `ManyRelatedManager`.


## Geos

The following are available only if there is an GEOS library accessible to Django.

### GeoJson

Return JSON field as GeoJSON.

```python
fields = {
    'location': fields.GeoJson
}
```

### EncodedPolyline

Return JSON field as an [encoded polyline](https://developers.google.com/maps/documentation/utilities/polylinealgorithm).

```python
fields = {
    'shape': fields.EncodedPolyline
}
```


## Create your own field type

If by any chance any of the above types don't work for your particular needs, you can create your own:

```python
fields = {
    'text': lambda x: x if len(x) <= 140 else text[:137]+"..."
}
```

Field types are functions that expect a single argument which is the result of `some_mode_instance.attribute` (or in the example above `some_model_instance.text`)
