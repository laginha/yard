# Meta options

As you have seen before it is mandatory for the Resource to have a Meta class declaring the bidding model, as follows:

```python
from yard.resources import Resource

class Foo(Resource):
    class Meta:
        model = Foo
```

However there are more options at your disposal.

- [Fields](meta/fields.md)
- [Serializers](meta/serializers.md)
- [Uglification](meta/uglification.md)
- [Pagination](meta/pagination.md)
- [Metadata](meta/metadata.md)
- [Documentation](meta/documentation.md)
