# Resource CRUD methods


```python
from yard import resources

class Foo(resources.Resource):

    class Meta:
        model = Foo

    def list(self, request):
        # GET /foo/
        return Foo.objects.all()

    def detail(self, request, pk):
        # GET /foo/:pk
        return Foo.objects.get(pk=pk)

    def create(self, request):
        # POST /foo/
        return 405

    def update(self, request, pk):
        # POST|PUT /foo/:pk
        return 405

    def destroy(self, request):
        # DELETE /foo/:pk
        return 405

    def new(self, request):
        # GET /foo/new/
        return 404

    def edit(self, request, pk):
        # GET /foo/:pk/edit/
        return 404
```

> **You only need to implement the methods you want**. By default *Yard* returns *405 Not Implemented*. However, if *Yard* realizes there is no need to add `foo/<pk>` to the urlpatterns (e.g. your resource only implements the method `list`), any access to that url pattern will naturally end up in a *404 Not found*.

Besides those 7 *Crud* methods, there is another one which is implemented by default: `options`. It returns a JSON documenting the resource according to the [Swagger specification](http://swagger.io/).

Moreover, it returns the *Allow* response header, with the allowable HTTP methods (e.g. `ALLOW: GET, POST, DELETE`)

---

As you have noticied in the example above, the *CRUD* methods may return any object as it is not limited to django's `HttpResponse`. You can return a `int` for status code or any other object (including model instance and querysets) for the response content.

For this feature, *Yard* mostly relies on [Django-Simple-Response app](https://github.com/laginha/django-simple-response). Check out [its documentation](https://github.com/laginha/django-simple-response/blob/master/docs/serialization.md).

