from django.forms import *
from alo.forms import QueryModelForm, QueryForm
from alo.operators import AND, OR

class Parameters(dict):
    
    @classmethod
    def create(cls, form=None):
        if form == None:
            parameters = cls()
            parameters.validated = {}
        elif isinstance(form, (QueryForm, QueryModelForm)):
            parameters = cls( form.parameters )
            parameters.validated = form.non_empty_data
        else:
            parameters = cls( form.cleaned_data )
            parameters.validated = dict([
                each for each in form.cleaned_data.items() if each[1]
            ])
        return parameters
