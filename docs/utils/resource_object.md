# The Resource Object


## Instance methods

### serialize

Serialize a model instance according to given fields. 

    self.serialize( ModelInstance, fields )

```python
from yard import resources

class BookResource(resources.Resource):

    def show(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        return {
            "API name": "Some API name",
            "Book": self.serialize( book, self.fields )
        }
```


### serialize_all

Serialize a `QuerySet` or list of model instances, according to given fields. 

    serialize_all( QuerySet, fields )

```python
from yard import resources

class BookResource(resources.Resource):

    def index(self, request, params):
        books = Book.objects.filter(**params)
        return {
            "API name": "Some API name",
            "Books": self.serialize_all( books, self.fields )
        }
```


### select_related

Optimize database access according to given fields.

    self.select_related( QuerySet, fields )

This method uses *django's* `QuerySet.select_related` method by guessing the necessary foreign-key relationships.

By default, *Yard* uses this method in every `QuerySet` based responses with the proper fields (`show_field` or `index_field`). 

```python
from yard import resources

class BookResource(resources.Resource):

    def index(self, request, params):
        books = Book.objects.filter(**params)
        return self.select_related( books, some_other_fields )
```


## Class attributes

### model

The model to which the resource is associated to. 

Although this attribute is optional it is very important for the hypermedia API to take full effect. Without it the *resource_uri*'s displayed in the *JSON* representation may not be correctly generated.

```python  
from yard import resources

class FooResource(resources.Resource):    
    model = Foo
```


### Meta

Nested class which attributes defines which metadata is added to each *GET* collection request (`index` method).

```python
from yard import resources    
    
class FooResource(resources.Resource):
    class Meta:
    	next_page = True
    	previous_page = True
        validated_parameters = True
```


### Pagination

Nested class which attributes defines the pagination for *GET* collection requests (`index` method).

```python  
from yard import resources

class FooResource(resources.Resource):    
    class Pagination:                    
        offset_parameter = 'offset'
        results_per_page = {       
            'parameter': 'limit',       
            'default': 100,
            'limit': 500,        
        }
```


## Instance attributes

### _api

The `Api` instance the `Resouce` belongs to.

```python 
from yard import resources

class FooResource(resources.Resource):
    def index(self, request, params):
    	foos = Foo.objects.all()
    	return {'resource_uri': self._api.get_uri(i) for i in foos}
```


### fields

Responsible for defining which returned model-instance's attributes are to be included in the *JSON* response. 

```python 
from yard import resources

class FooResource(resources.Resource):
    fields  = ('id', 'bar')
```


### index_fields

Same as `fields` but for the `index` method only. It has priority over `fields`. 

```python 
from yard import resources

class FooResource(resources.Resource):
    index_fields  = ('id',)
```


### show_fields

Same as `fields` but for the `show` method only. It has priority over `fields`. 

```python 
from yard import resources

class FooResource(resources.Resource):
    show_fields  = ('id', 'bar' )
```

### description

Description of the resource. Used in the *discover* option of the *Api*.

```python 
from yard import resources

class FooResource(resources.Resource):
    description = "This resource is responsible for foo"
```

