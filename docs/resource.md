# Resource

A rather simple yard-based resource looks like this:

<pre>
class My_Resource(Resource):
    parameters = (...)
    fields     = (...)

    @staticmethod
    def index(request, params):
        ...

    @staticmethod
    def show(request, book_id):
        ...
</pre>

## Resource Methods

*Yard* resource supports automatically the following crud methods:

<table border="1">
    <tr>
        <th>Resource Method</th>
        <th>HTTP Method</th>
        <th>URL</th>
    </tr>
    <tr>
        <td>index</td>
        <td>Get</td>
        <td>/myresource/</td>
    </tr>
    <tr>
        <td>show</td>
        <td>Get</td>
        <td>/myresource/:id/</td>
    </tr>
    <tr>
        <td>create</td>
        <td>Post</td>
        <td>/myresource/</td>
    </tr>
    <tr>
        <td>update</td>
        <td>Put</td>
        <td>/myresource/:id/</td>
    </tr>
    <tr>
        <td>destroy</td>
        <td>Delete</td>
        <td>/myresource/:id/</td>
    </tr>
</table>

All you need to do is to include the resource in the urlpatterns.

*urls.py*
<pre>
from yard.urls import include_resource

urlpatterns = patterns('',
    url( r'^myresource', include_resource( My_Resource ) ),
)
</pre>

### Responses

Supported return types:

<table border="1">
    <tr>
        <th>Support Type</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>QuerySet</td>
        <td>Returns JSON-response (list) according to attribute fields</td>
    </tr>
    <tr>
        <td>Model Instance</td>
        <td>Returns JSON-response according to attribute fields</td>
    </tr>
    <tr>
        <td>ValuesQuerySet</td>
        <td>Defines content of JSON-response</td>
    </tr>
    <tr>
        <td>int</td>
        <td>Defines the HTTP-response's status code (defaults to 200)</td>
    </tr>
    <tr>
        <td>str</td>
        <td>Defines content of JSON-response</td>
    </tr>
    <tr>
        <td>dict</td>
        <td>Defines content of JSON-response</td>
    </tr>
    <tr>
        <td>list</td>
        <td>Defines content of JSON-response</td>
    </tr>
    <tr>
        <td>file</td>
        <td>Returns a HTTP-response as file like object</td>
    </tr>
    <tr>
        <td>None</td>
        <td>Defaults to HTTP-response</td>
    </tr>
    <tr>
        <td>tuple</td>
        <td>
            First value defines HTTP-response's status.
            Second value defines content as explained above.
        </td>
    </tr>
    <tr>
        <td>HttpResponse</td>
        <td>Returns HttpResponse as it is</td>
    </tr>
</table>

*example*
<pre>
class Book(Resource):

    @staticmethod
    def create(request):
        return 401, 'Not Authorize'
</pre>

Moreover, due to the fact *Yard* applies the attribute *fields* (as explained below) in every *QuerySet* or model instance response, you are always limited to return resources of the same base model. Which means

<pre>
class Book(Resource):

    @staticmethod
    def index(request, params):
        return Book.objects.filter(**params)
    
    @staticmethod
    def show(request, book_id):
        return Author.objects.filter(id=book_id)
</pre>

won't work properly.


## Fields

Yard-resource has attribute named *fields* (inspired in Django-Piston). It is a nested tuple, where you define which attributes of your base-model you wish to be included in the JSON response when requested **index** or **show**.

<pre>
class Book(Resource):
    fields = ('id', 'title', ('author', ('name',)) )
    
    @staticmethod
    def show(request, book_id):
        return Book.objects.filter(id=book_id)
</pre>

In this example, we have a resource named *Book*. Only the *show* method is implemented and returns a QueryField of base model *Book*. A client, when requesting *GET: http://example/books/id/* will receive a JSON response built according to the specified *fields* attribute.

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

In fact, *id* and *title* are attributes of model *Book*, as well as *author* which is a foreign key field to model instance *Author*, that has attribute *name*.

### Instance methods in fields

Specified fields can also be instance methods, as long as they are callable with no arguments besides instance. This is a good way to include data into the JSON response which can't be specified directly through the model's attributes.

<pre>
class Book(models.Model):
    ...
    genres = models.ManyToManyField( Genre )
    
    def book_genres(self):
        return self.genres.all()
        #return self.genres.all().values()

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


## Parameters

Another attribute of the Yard resource is *parameters*, which is only used in the **index** method. It is its purpose to control, in a neat way, the logic for acceptable parameters in each requests.

<pre>
class Book(Resource):
    parameters = (
        { 'name': 'author', 'alias': 'author__id' },
        { 'name': 'title' },
    )

    @staticmethod
    def index(request, params):
        return Book.objects.filter( **params )
</pre>

In this example, there are two allowed parameters. Both are not required and can be used simultaneous or separated. If any of these parameters is in request, it will assume the name specified in 'alias'. This key is meant to facilitate database querying in the server side.

For each parameter the following keys can be defined:

<table border="1">
    <tr>
        <th>Key</th>
        <th>Demand</th>
        <th>Type</th>
        <th>Definition</th>
    </tr>
    <tr>
        <td>name</td>
        <td>Required</td>
        <td>String</td>
        <td>Name of the parameter for API clients</td>
    </tr>
    <tr>
        <td>alias</td>
        <td>Not required</td>
        <td>String</td>
        <td>Parameter's name within server's logic</td>
    </tr>
    <tr>
        <td>required</td>
        <td>Not required</td>
        <td>Boolean</td>
        <td>Whether parameter is required or not</td>
    </tr>
    <tr>
        <td>limit</td>
        <td>Not required</td>
        <td>Single-arg callable (lambdas)</td>
        <td>Logic which the parameter has to oblige to</td>
    </tr>
</table>

Moreover, the *parameters* attribute supports boolean logic: AND, OR. This allows more complex API's to be implemented easily.

<pre>
class Books(Resource):
    parameters = (
        { 'and': (
            { 'name': 'title', },
            { 'or': (
                { 'name':  'author', 
                  'alias': 'author__id' },                                      
                { 'name':  'year',
                  'alias': 'publication_date__year',
                  'limit': lambda x: x&le;2012 and x&ge;1970 }, 
            )}, 
        )}, 
    )
</pre>

In this example, the given parameters have to obey the logic: *title* AND (*author* OR *year*). 

Notice that the parameter *year* has the key *limit* which demands for the parameter's value to be between 1970 and 2012. If this verification fails, the parameter is ignored. (Note: *Yard* detects if parameter's value is whether float or int and automatically converts it before passing it through *limit*)

