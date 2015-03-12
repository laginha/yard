# Meta options

As you have seen before it is mandatory for the Resource to have a Meta class declaring the bidding model, as follows:

```python
from yard.resources import Resource

class Foo(Resource):
    class Meta:
        model = Foo
```

However there are more options at your disposal.

- [Fields](fields.md)
- [Serializers](serializers.md)
- [Uglification](uglification.md)
- [Pagination](pagination.md)
- [Metadata](metadata.md)
- [Documentation](documentation.md)
