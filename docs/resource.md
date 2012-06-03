# Resource

The *Resource* object represents the resource data you wish to provide access to. Its main purposes are:

- organize the different crud methods into its instance methods. 
- simplify your http responses, returning JSON whenever possible (see [responses.md](responses.md)).
- structure your JSON resource response, according to class attribute *fields* (see [fields.md](fields.md))..
- parse input according to class attribute *parameters* (see [forms.md](working_with_forms/forms.md)).

In the end, your resource might look like this: 

<pre>
class MyResource(Resource):
    parameters = ...
    fields     = (...)

    def index(self, params):
        return {'foo':'bar'}

    def show(self, book_id):
        return 404
</pre>

For the resource to be accessible you will need to include it in the url patterns:

<pre>
from yard.urls import include_resource

urlpatterns = patterns('',
    url( r'^myresource', include_resource( My_Resource ) ),
)
</pre>


## CRUD instance methods

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

If any of these methods is not implemented, *Yard* returns *Not Found* whenever requested.

