# Pagination

Although *Yard* does not paginate *QuerySet* based responses by default, it provides a way to set it up.

<pre>
class Books(Resource):
    
    class Page:                    
        offset_parameter = 'offset'
        results_per_page = {       
            'default': 25,         
        }
    
    def index(self, params):
        # params does not include the 'offset' parameter
        ...
</pre>


## Page Options

### offset_parameter

    offset_parameter = 'offset'

- name of the parameter for the offset number. (REQUIRED)

### results_per\_page

    results_per_page = {
        'parameter': 'results',       
        'default': 25,
        'limit': 50,      
    }

- **default**: default number of results per each page. (REQUIRED)
- **parameter**: name of the parameter for the number of results.
- **limit**: maximum number of results per each page allowed. If *parameter* not defined, *limit* is ignored.
