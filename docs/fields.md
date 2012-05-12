# Fields

The *fields* attribute is responsible for defining which returned model's attributes are to be included in the JSON response (only used for **index** and **show** methods only). 

For this attribute is expected a tuple of strings and tuples. While the former type indicates a model attribute's name, the latter is meant to dive into a foreign key instance as follows:

    ('name of the fk attribute',('fk intance attribute1', 'fk intance attribute2'))

In the example below the resource named *BookResource* implements the *show* method which returns a QueryField for base model *Book*.

<pre>
class BookResource(Resource):
    fields = ('id', 'title', ('author', ('name',)) )
    
    @staticmethod
    def show(request, book_id):
        return Book.objects.filter(id=book_id)
</pre>

The API client, whenever requesting *GET: http://example/books/id/*, will receive a JSON response built according to the specified *fields* attribute.

<pre>
[ 
    { "id": "8",
      "name": "A Game of Thrones",
      "author": {
          "name": "George R.R. Martin",
      }
    } 
]
</pre>


## Instance methods in fields

*Fields* elements of type string can also indicate instance methods, as long as they are callable with no arguments besides instance. This is a good way to include data into the JSON response which can't be specified directly through model's attributes.

<pre>
class Book(models.Model):
    ...
    genres = models.ManyToManyField( Genre )
    
    def book_genres(self):
        return self.genres.all()

class Book(Resource):
    fields = ('id', 'title', 'book_genres', ('author', ('name',)) )
</pre>

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
