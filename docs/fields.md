# Fields

The *fields* attribute is responsible for defining which returned model's attributes are to be included in the JSON response (only used for **index** and **show** methods only). If not defined all model's attributes will be used.

For this attribute is expected a tuple of strings and tuples. While the former type indicates a model attribute's name, the latter is meant to dive into a foreign key instance as follows:

    ('name of the fk attribute',('fk intance attribute1', 'fk intance attribute2'))

Also, *Yard* allows you to define different *fields* for the *show* and *index* methods, by means of *show\_fields* and *index\_fields* attributes.

In the example below the resource named *BookResource* implements the *show* method which returns a QueryField for base model *Book*.

```python
class BookResource(Resource):
    fields = ('id', 'title', ('author', ('name',)) )
    
    def show(self, book_id):
        return Book.objects.filter(id=book_id)
```

The API client, whenever requesting *GET: http://example/books/id/*, will receive a JSON response built according to the specified *fields* attribute.

```javascript
[ 
    { "id": "8",
      "name": "A Game of Thrones",
      "author": {
          "name": "George R.R. Martin",
      }
    } 
]
```



## Instance methods in fields

*Fields* elements of type string can also indicate instance methods. This is a good way to include data into the JSON response which can't be specified directly through model's attributes.

```python
class Book(models.Model):
    ...
    genres = models.ManyToManyField( Genre )
    
    def book_genres(self):
        return self.genres.all()

class Book(Resource):
    fields = ('id', 'title', 'book_genres', ('author', ('name',)) )
```

The instance method can be callable with arguments. You just need to indicate the argument in front of the instance method name, within the string field

    fields = 'method arg0 arg1'

*Yard* deals differently with different object types returned by instance methods:

<table border="1">
    <tr>
        <th>Allowed types</th>
        <th>Process</th>
    </tr>
    <tr>
        <td>ValuesQuerySet</td>
        <td>Converts to json</td>
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
        <td>other (e.g. model instance)</td>
        <td>Unicodes value</td>
    </tr>
</table>
