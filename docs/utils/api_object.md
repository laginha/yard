# The API object

This *Object* is responsible to generate the *urlpatterns* according to its *Resources*.


### init

The class constructor accepts one argument that defines the pre-path of its *Resources* (defaults to `r'^`)

```python
api = Api( path=r'^apipath/' )
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
get_uri( model )
```

Arguments:

- **model**: model associated to a *Resource*

Example:

```python
get_uri( Foo )
```
