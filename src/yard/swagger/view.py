from django.views.generic.base import TemplateView
from yard.swagger import consts

class SwaggerUIView(TemplateView):
    template_name = 'swagger_index.html'

    def get_context_data(self, **kwargs):
        context = super(SwaggerUIView, self).get_context_data(**kwargs)
        context['options'] = consts
        return context