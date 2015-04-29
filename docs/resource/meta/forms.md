# Forms

## query_form

```python
from yard.resources import Resource

class Foo(Resource):
    class Meta:
        query_form = FooForm
```

which is the same as

```python
from yard.resources import Resource
from yard.resources import Resource

class Foo(Resource):

    @validate(FooForm)
    def list(self, request):
        ...
```

This alternative is useful specially if you want to change only the query form between resource versions.


## create_form

The same as `query_form` but for the `create` resource method.

## update_form

The same as `query_form` but for the `update` resource method.

