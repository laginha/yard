from django.contrib           import admin
from yard.apps.keyauth.models import Key, Consumer

admin.site.register( Key )
admin.site.register( Consumer )
