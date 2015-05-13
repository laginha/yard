# Metadata

Whenever a Resource's **list** method returns a `QuerySet`, a list of model instances or a `ValuesSet`, *Yard* appends useful metadata by default to the resulting JSON representation.


```python  
from yard import metadata

class BookMetadata(metadata.Metadata): 
    validated_parameters = False
    maximum = (('longest_title', 'title'),)
```

```python 
from yard import resources

class Book(resources.Resource):
    class Meta:
        model = models.Book
        metadata = BookMetadata
```

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
        ...
    ], 
    "Meta": {
        "longest_title": "A Feast for Crows",
        "next_page": /books/?offset=25,
        "previous_page": /books/?offset=25,
        "paginated_objects": 25
        "total_objects": 30, 
        "longest_title": "A Feast for Crows",
    }
}
```


## Metadata Options


### total_objects

    total_objects = True

- if set to `True`, adds the number of instances returned by the `QuerySet` to the *JSON* response.
- defaults to `True`.

### paginated_objects

    number_of_objects = True

- if set to `True`, adds the number of instances returned by the paginated `QuerySet` to the *JSON* response.
- defaults to `True`.

### next_page

    next_page = True

- if set to `True`, adds the url path for the next page to the *JSON* response.
- defaults to `True`.

### previous_page

    previous_page = True

- if set to `True`, adds the url path for the previous page to the *JSON* response.
- defaults to `True`.

### validated_parameters

    validated_parameters = True

- if set to `True`, adds validated parameters for filtering to the *JSON* response. 
- defaults to `True`.

### no_meta

    no_meta = True

- if set to `True`, no metadata is included in the *JSON* response.
- defaults to `False`.

### average

    average = (('average_pages', 'number_of_pages'),)
    
- adds result of: `QuerySet.aggregation(average_pages = Avg('number_of_pages'))`

### maximum

    maximum = (('longest_title', 'title'),)
    
- adds result of: `QuerySet.aggregation(longest_title = Max('title'))`

### minimum

    minimum = (('smallest_title', 'title'),)
    
- adds result of: `QuerySet.aggregation(smallest_title = Min('title'))`
    
### count

    count = (('count_pages', 'number_of_pages'),)

- adds result of: `QuerySet.aggregation(count_pages = Count('number_of_pages'))`


## Customize

If the available options are not enough for your needs, it is possible to create your own metadata. For example:

    smallest_title = lambda x: x.aggregation(Min('title'))
    
Custom-made meta option needs to be callable with a single argument, which is a the *QuerySet*.
