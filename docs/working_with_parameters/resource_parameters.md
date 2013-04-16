# ResourceParameter

The third argument of the `index` method is a `ResourceParameters` instance.

```python
    def index(self, request, params):
        ...
```


## Methods

The `ResourceParameter` class provides a small set of methods:


### is_valid

Returns `True` if there was no error while fetching parameters from the http request. Otherwise, returns `False`.


### errors

Returns a dictionary with the errors detected while fetching parameters from the http request.

- `RequiredParamMissing`: required parameter not found in request.
- `InvalidParameterValue`: parameter value failed the validation test.
- `ConversionError`: parameter value could not be properly converted.
- `AndParameterException`: all parameters within an AND were not met/validated.


### from_path

Returns dictionary of parameters of type path (given in the url).


### from_query

Returns dictionary of parameters of type query.


## Example

```python
from yard import resources, forms

class BookResource(resources.Resource):
    class Parameters:
        ...

    def index(self, request, params):
        if params.is_valid():
            return Book.objects.filter( **params )
        return params.errors()
```

In this example, the model is filtered only if there was no error detected, according to the `Parameters` logic, while validating the given request input. However, such verification can be ignored since **only the validated parameters are used in filter**.

As an alternative to the example above, you can use the `validate` decorator instead.

```python
from yard.resources.decorators import validate
from yard import resources, forms

class BookResource(resources.Resource):
    class Parameters:
        ...

    @validate
    def index(self, request, params):
        return Book.objects.filter( **params )
```
