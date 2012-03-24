from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^',       include('example.book_store.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
