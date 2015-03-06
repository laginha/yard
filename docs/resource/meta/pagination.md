# Pagination

The *Yard* framework paginates `QuerySet`, `ValueSet`, `list` and `generator` based responses, **but only in requests that hit the Resource's list method**.

```python  
from yard import pagination

class BookPagination(pagination.Pagination): 
    results_parameter = 'number'
    results_per_page = 25
    limit_per_page = 100
```

```python 
from yard import resources

class Book(resources.Resource):
    class Meta:
        model = models.Book
        pagination = BookPagination
```


## Pagination Options

### no_pagination

- disable pagination in the resource.
- defaults to `False`

### offset_parameter

- name of the parameter for the offset number.
- defaults to *offset*.

### results_parameter

- name of the parameter for the number of results
- defaults to *results*.

### results_per\_page

- default number of results per each page. 
- defaults to *25*.

### limit_per\_page

- maximum number of results per each page allowed
- defaults to *50*.
