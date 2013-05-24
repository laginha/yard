# The API object

This *Object* is responsible to generate the *urlpatterns* according to its *Resources*.


### init

The class constructor accepts two arguments:

- **path**: defines the pre-path of its *Resources* (defaults to `r'^`)
- **discover**: defines if the pre-path should return a list of available resources in the *Api* (defaults to `False`)

```python
api = Api( r'^apipath/', discover=True )
```

In this case a *HTTP GET* request to `http://example.com/apipath` would return a *JSON* response like this:

```javascript
{
    Resources: [
        {
            uri: "some_resource/"
            description: "some description"
        },
        ...
    ]
}
```

## Methods and Properties

### urlpatterns

Get the generated url patterns.

Example:

```python
api.urlpatterns
```


### include

Add a *Resource* to the API

```python
include( resource_path, resource_class, single_name=None, collection_name=None )
```

Arguments:

- **resource_path**: URI path of the resource.
- **resource_class**: the *Resource* class you want to add.
- **single_name**: viewname for `/path/to/resource/:id`.
- **collection_name**: viewname for `/path/to/resource/`.

Example:

```python
api.include( r'foo', FooResource )
```


### extend

Add the `urlpatterns` from another *urls*.

```python
extend( path, to_include, name=None )
```
	
Arguments:

- **path**: URI path to the new `urlpatterns`.
- **to_include**: path to the other *urls*.
- **name**: name of the url pattern.

Example:

```python
api.extend( r'someapp', 'path.to.someapp.urls' )
```


### get_uri

Get URI path of the resource associated the a given model. For this to work properly the expected *Resource* must have the class attribute `model`.

```python
get_uri( modelinstance )
```

Arguments:

- **modelinstance**: model associated to a *Resource*

Exceptions:

- **yard.exceptions.NoResourceMatch**: There is no *Resource* associated with the model.
- **django.core.urlresolvers.NoReverseMatch**: Although there is a *Resource* associated with the model there is no *URL* match for the model instance.

Example:

```python
get_uri( foo )
```
