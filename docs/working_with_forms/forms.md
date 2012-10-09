# Forms

The *Yard* resource relies on the *parameters* attribute for the **index** method. Its purpose is to filter and process the http request parameters according to a given *yard form*.

<pre>
class BookResource(Resource):
    parameters = BookParameters

    def index(self, request, params):
        return Book.objects.filter( **params )
</pre>

you can also use forms as a nested class within *Resource*:

<pre>
class BookResource(Resource):
    
    class Parameters(Form):
        ...

    def index(self, request, params):
        return Book.objects.filter( **params )
</pre>



Very much like *django forms*, you can include any [parameter type](parameters.md) as a form attribute. However there is a special attribute, *__logic__*, where you can easily define logic between parameters for a particular API method.

<pre>
from yard.forms import *

class BookParameters(Form):
    year   = IntegerParam( alias='publication_date__year', min_value=1970, max_value=2012 )
    title  = CharParam()
    author = CharParam( alias='author__name' )

    __logic__ = year, title & (author | year)
</pre>

In this example, the *year* parameter is allowed as well as the combined presence of *title* and either *author* or *year* parameters. 

As you have noticed, each form's parameter can be reused in different logic sentences. 


### Tips

For *DateParam* you may want to default it to the current day. Do it so the default value is callable, like this:

    from datetime import date
    DateParam( default = date.today )

otherwise the default will correspond to the day in which the server was started.

