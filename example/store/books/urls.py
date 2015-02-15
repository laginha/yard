from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from yard.api import Api
from .resources import AuthorResource, BookResourceVersions

api = Api(discover=True)
api.include( 'books', BookResourceVersions )
api.include( 'authors', AuthorResource )

urlpatterns = api.urlpatterns
urlpatterns += patterns('',
    url(r'^doc/', include('yard.swagger.urls')),
)

if settings.DEBUG:
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    