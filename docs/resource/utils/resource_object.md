# The Resource Object


### api

The `Api` instance the `Resource` belongs to.

### version_name

Name given to the `Resource` when versioned with `VersionController`. 

### _meta

Copy of `Resource.Meta` but with its attributes instantiated. (Created per request)


### serialize()

Serialize a model instance according to given fields. 

```python
self.serialize( ModelInstance, fields )
```

### serialize_all()

Serialize a `QuerySet` or list of model instances, according to given fields. 

```python
serialize_all( QuerySet, fields )
```

### select_related()

Optimize database access according to given fields, by using *django's* `QuerySet.select_related` and `QuerySet.prefetch_related`. By default, *Yard* uses this method in every `QuerySet` based responses.

```python
self.select_related( QuerySet, fields )
```

*Yard* infers the relationships by analyzing the given *fields* and its *field types*. Therefore the latter plays a major role in this process. For instance

```python
fields = {
    'author': fields.Unicode
}
```

and

```python
fields = {
    'author': fields.ForeignKey
}
```

result in the same *JSON* response

```javascript
{
    "Objects": [
        {
            'author': "George R. Martin",
        }...
    ]...
}
```

However, with the latter *Yard* is able to recognize the relation and adds `author` to `select_related`. In other words, it performs fewer database queries, hence is faster.
