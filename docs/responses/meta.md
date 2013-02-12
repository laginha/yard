# Metadata

```python
class Books(Resource):

    class Meta:
        with_errors = True
        ...
```

For *QuerySet*, *list* and *ValuesSet* based responses, *Yard* appends useful metadata by default:

- **total_objects**: number of instances returned after filtering.
- **parameters_considered**: parameters validated for filtering.

```javascript
{
  "Objects": [
    {
      "publication_date": "2005-10-17", 
      "author": {
        "name": "George R.R. Martin", 
      }, 
      "title": "A Feast for Crows"
    }, 
  ], 
  "Meta": {
    "total_objects": 2, 
    "parameters_considered": {}, 
  }
}
``


## Meta Options

### no_meta

    no_meta = True

- no metadata is included in the JSON response, if *True*.
- defaults to *False*.

### with_errors

    with_errors = True

- adds parameters' validation errors to the JSON response, if *True*.
- defaults to *False*.

### total_objects

    total_objects = True

- adds the number of instances returned by the QuerySet to the JSON response, if *True*.
- defaults to *True*.

### paginated_objects

    number_of_objects = True

- adds the number of instances returned by the paginated QuerySet to the JSON response, if *True*.
- defaults to *True*.

### validated_parameters

    validated_parameters = True

- adds validated parameters for filtering to the JSON response, if *True*. 
- defaults to *True*.

### average

    average = (('average_pages', 'number_of_pages'),)
    
- adds result of: *QuerySet.aggregation(average_pages = Avg('number_of_pages'))*

### maximum

    maximum = (('longest_title', 'title'),)
    
- adds result of: *QuerySet.aggregation(longest_title = Max('title'))*

### minimum

    minimum = (('smallest_title', 'title'),)
    
- adds result of: *QuerySet.aggregation(smallest_title = Min('title'))*
    
### count

    count = (('count_pages', 'number_of_pages'),)

- adds result of: *QuerySet.aggregation(count_pages = Count('number_of_pages'))*


## Customize

If the available options are not enough for your needs, it is possible to create your own meta.

    smallest_title = lambda x: x.aggregation(Min('title'))
    
Custom-made meta option need to be callable with a single argument, the *QuerySet*.
    