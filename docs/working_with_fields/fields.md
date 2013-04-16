# Fields

The `fields` attribute is responsible for defining which returned model instance's attributes are to be included in the *JSON* response. 

if the `model` attribute is defined in the `Resource`, `fields` defaults to all model's attributes.


## Instance attributes in fields

```python 
from yard import resources, fields

class BookResource(resources.Resource):
    fields = {
        'id': fields.Integer, 
        'title': fields.Unicode, 
        'author': fields.Unicode
    }
```

The API-client, whenever requesting a resource collection (`index`), will receive a *JSON* response built according to the specified `fields` attribute.

```javascript
{
    "Objects": [
        {
            "id": "1", 
            "author": "George R.R. Martin",
            "title": "A Feast for Crows"
        }, 
        ...
    ], 
    "Meta": {
        ...
    }
}
```


## Foreign keys in fields

It is also possible to dive into a foreign key instance, as follows:

```python 
from yard import resources, fields

class BookResource(resources.Resource):
    fields = {
        'id': fields.Integer, 
        'title': fields.Unicode, 
        'author': {
            'age': fields.Integer,
            'name': fields.Unicode
        }        
    }
```

resulting in the following *JSON* response:

```javascript
[ 
    { "id": "8",
      "title": "A Game of Thrones",
      "author": {
          "id": 1,
          "name": "George R.R. Martin",
      }
    } 
]
```

resulting in the following *JSON* response:

```javascript
[ 
    { "id": "8",
      "title": "A Game of Thrones",
      "author": {
          "id": 1,
          "name": "George R.R. Martin",
      }
    } 
]
```


## Instance methods in fields

`fields` elements can also indicate instance methods. This is a good way to include data into the *JSON* response which can't be specified directly through model's attributes.

The instance method can be callable with arguments. You just need to indicate the arguments in front of the instance method name: `method_name arg0 arg1`.

```python
from django import models
from yard import resources, fields

class Book(models.Model):
    ...
    genres = models.ManyToManyField( Genre )
    
    def book_genres(self):
        return self.genres

class Book(resources.Resource):
    fields = {
        'id': fields.Integer, 
        'title': fields.Unicode, 
        'book_genres': fields.RelatedManager, 
        'author': fields.Unicode
    }
```


Beware, *Yard* deals differently according to the object type returned by instance methods:

<table border="1">
    <tr>
        <th>Object types</th>
        <th>Process</th>
    </tr>
    <tr>
        <td>ValuesQuerySet</td>
        <td>Converts to list</td>
    </tr>
    <tr>
        <td>QuerySet</td>
        <td>Converts to list</td>
    </tr>
    <tr>
        <td>JSON-serializable (e.g. dict, list)</td>
        <td> - </td>
    </tr>
    <tr>
        <td>Other (e.g. model instance)</td>
        <td>Converts to unicode</td>
    </tr>
</table>


## Dynamic fields

Some times it is required that the resource's representation to depend on the given input in the request. For that purpose, the `fields` attribute can be callable and should expect the validated parameters (`ResourceParameters`) as it argument.

```python 
from yard import resources

class BookResource(resources.Resource):
    
    def fields(self, params):
        if params.pop('withauthor', False):
            return {
                'id': fields.Integer, 
                'title': fields.Unicode, 
            }
        return {
            'id': fields.Integer, 
            'title': fields.Unicode, 
            'author': fields.Unicode
        }
```


## Show and index fields

*Yard* allows you to define different *JSON* representation for the `show` and `index` methods, by means of `show\_fields` and `index\_fields` attributes. These attributes have priority over the `fields` attribute.

```python 
from yard import resources, fields

class BookResource(resources.Resource):
    list_fields = {
        'id': fields.Integer, 
    }
    detail_fields = {
        'id': fields.Integer, 
        'title': fields.Unicode, 
        'author': {
            'name': fields.Unicode
        }
    }    
```

