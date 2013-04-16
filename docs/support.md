# Supported return types

<table border="1">
    <tr>
        <th>Object Type</th>
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
        <td>generator</td>
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
            First value defines HTTP-response's status (int).
            Second value defines content as explained above.
        </td>
    </tr>
    <tr>
        <td>HttpResponse</td>
        <td>Returns HttpResponse as it is</td>
    </tr>
</table>


## Examples

```python
from yard import resources

class BookResource(resources.Resource):
    def create(self):
        return 401, 'Not Authorize'
```

```python
class BookResource(resources.Resource):
    def destroy(self, request):
        return 401
```

```python
class BookResource(resources.Resource):
    def show(self, request, book_id):
        return Book.objects.get(id=book_id)
```
