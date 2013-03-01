# Parameters

The *Yard* resource relies on the `Parameters` attribute for the `index` method. Its purpose is to filter and process the given http request input.


## Basic

Include several [parameter types](params.md) as an attribute.

<pre>
```python
from yard import resources, forms    
    
class BookResource(resources.Resource):
    class Parameters:
        title  = forms.CharParam()
        author = forms.CharParam()

    def index(self, request, params):
        return Book.objects.filter( **params )
```
</pre>

The attributes names are the inputs expected for the API.

	http://example.com/books/?title=whatever&author=someauthor
	
and the code line `Book.objects.filter( **params )` in the example above, is in fact `Book.objects.filter( title=whatever, author=someauthor )`.

### alias
	
The *param* name is often not equal to the model field name. When that is the case, use an `alias` as follows:

<pre>
```python
from yard import resources, forms    
    
class BookResource(resources.Resource):
    class Parameters:
        year = forms.IntegerParam( alias='publication_date__year' )

    def index(self, request, params):
        return Book.objects.filter( **params )
```
</pre>

As before, the attributes names are the inputs expected for the API.

	http://example.com/books/?year=2013

However the code line `Book.objects.filter( **params )` corresponds to `Book.objects.filter( publication_date__year=2013 )`.


## Logic

There is a optional, yet powerful attribute named `__logic__`. It is meant to easily define the logic between parameters for a particular API method.

<pre>
```python
from yard import resources, forms    

class BookResource(resources.Resource):
    class Parameters:
        year   = forms.IntegerParam()
        title  = forms.CharParam()
        author = forms.CharParam()

        __logic__ = year, title, author & (year | title)
```
</pre>

In this example, the *year*, and *title* parameter are allowed as well as the combined presence of the parameters *author* and either *year* or *title*.

