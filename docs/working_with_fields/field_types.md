# List of types



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

Alias for ´fields.ict´

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

### GeoJSON

Return JSON field as GeoJSON.

```python
fields = {
    'location': fields.GeoJson
}
```

### RelatedManager

Return JSON field as a list of unicode values for RelatedManager input.

```python
fields = {
    'authors': fields.RelatedManager
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
    'id': fields.URI
}
```    
    
This type expects a *model instance* as input which `Model` is referenced by a `Resource`.

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


### get\_field

Return JSON field with the type most appropriated for the input.

```python
fields = {
    'id': fields.get_field
}
```

If you are too lazy to specify the field type, this is a good solution for you. However This may not work properly for instance method based field.


## Create your own field type

If by any chance any of the above types don't work for your particular needs, you can create your own:

```python
fields = {
    'description': lambda data: text if len(text) <= 140 else text[:140]+"..."
}
```

Field types are functions that expect a single argument which is the result of `some_mode_instance.attribute` (or in the example above `some_model_instance.text`)
