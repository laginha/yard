from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
# from django.core.urlresolvers import reverse


urlpatterns = patterns('',
    url(r'^$', 
        TemplateView.as_view(template_name = "swagger_index.html"), 
        name='swagger',
    ),
)
