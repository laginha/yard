# ResourceParameters

The second argument of the *index* method is a ResourceParameters instance. It provides a small set of methods:

- **is_valid():**   Returns True if there was no error while fetching parameters from the http request. Otherwise, returns False.
- **errors():**     Returns a dictionary with the errors detected while fetching parameters from the http request.
- **from_path():**  Returns dictionary of parameters of type path, as defined in the url pattern.
- **from_query():** Returns dictionary of parameters of type query.

<pre>
class BookResource(Resource):
    parameters = BookParameters()

    @staticmethod
    def index(request, params):
        if params.is_valid():
            return Book.objects.filter( **params )
        return params.errors()
</pre>

In the example above, *filter* is executed only if *params* is valid. However, such verification can be ignored since only the validated parameters are added to the ResourceParameters instance. In this case, any error that might have occurred is ignored.

<pre>
class BookResource(Resource):
    parameters = BookParameters()

    @staticmethod
    def index(request, params):
        return Book.objects.filter( **params )
</pre>