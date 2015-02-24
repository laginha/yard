from django.conf.urls import patterns, include, url
from .view import SwaggerUIView

urlpatterns = patterns('',
    url(r'^$', SwaggerUIView.as_view(), name='swagger'),
)
