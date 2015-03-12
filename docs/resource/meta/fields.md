# Fields

The `fields` meta attribute is responsible for defining which returned model instance's attributes are to be included in the *JSON* response. It defaults to all the Resource's related model's attributes.

```python 
from yard import resources, fields

class Book(resources.Resource):
    class Meta:
        model = models.Book
        fields = {
            'id': fields.Integer, 
            'title': fields.Unicode, 
            'author': fields.Unicode
        }
        
    def list(self, request):
        return Book.objects.all()
```

The API-client, whenever requesting a resource collection (`list`), will receive a *JSON* response built according to the specified `fields` attribute.

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

> Because `fields.Integer` and `fields.Unicode` are not enough, **see the [list of all available field types](field_types.md)!**


## Foreign keys in fields

It is also possible to dive into a foreign key instance, as follows:

```python 
from yard import resources, fields

class Book(resources.Resource):
    class Meta:
        model = Book
        fields = {
            'title': fields.Unicode, 
            'author': {
                'age': fields.Integer,
                'name': fields.Unicode
            }  
        }   
```


resulting in the following *JSON* response:

```javascript
{
    "Objects": [
        {
            "author": {
            	"age": 67
                "name": "George R.R. Martin", 
            }, 
            "title": "A Feast for Crows"
        }, 
        ...
    ], 
    "Meta": {
        ...
    }
}
```

## Instance methods in fields

`fields` elements can also indicate instance methods. This is a good way to include data into the *JSON* response which can't be specified directly through model's attributes.

The instance method can be callable with arguments. You just need to indicate the arguments in front of the instance method name: `method_name arg0 arg1`.

```python
from django import models

class Book(models.Model):
    ...
    genres = models.ManyToManyField( Genre )
    
    def book_genres(self):
        return self.genres
```

```python
from yard import resources, fields

class Book(resources.Resource):
    class Meta:
        model = models.Book
        fields = {
            'id': fields.Integer, 
            'title': fields.Unicode, 
            'book_genres': fields.RelatedManager, 
            'author': fields.Unicode
        }
```


## Dynamic fields

Some times it is required that the resource's representation to depend on the given input in the request. For that purpose, the `fields` attribute can be callable and should expect django's `Request` as its argument.

```python 
from yard import resources

class Book(resources.Resource):
    class Meta:
        model = models.Book
        
        def fields(self, request):
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


## Detail and List fields

*Yard* allows you to define different *JSON* representation for the `detail` and `list` methods, by means of `detail\_fields` and `list\_fields` meta attributes. These attributes have priority over the `fields` attribute.

```python 
from yard import resources, fields

class BookResource(resources.Resource):
    class Meta:
        model = models.Book
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
