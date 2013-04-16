# Pagination

The *Yard* framework paginates `QuerySet`, `ValueSet`, *list* and *generator* based responses. This behavior is **compulsory**.

```python  
from yard import resources

class FooResource(resources.Resource):
    
    # default configuration
    class Pagination:                    
        offset_parameter = 'offset'
        results_per_page = {       
            'parameter': 'results',       
            'default': 25,
            'limit': 50,        
        }
```


## Pagination Options


### offset_parameter

    offset_parameter = 'offset'

- name of the parameter for the offset number.
- defaults to *offset*.

### results_per\_page

    results_per_page = {
        'parameter': 'limit',       
        'default': 50,
        'limit': 100,      
    }

- **default**: default number of results per each page. Defaults to *25*.
- **parameter**: name of the parameter for the number of results. Defaults to *results*.
- **limit**: maximum number of results per each page allowed. Defaults to *100*.
