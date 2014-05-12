from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve as serve_static
from django.contrib import admin

from main.views import *

admin.autodiscover()

urlpatterns = patterns('',              
    #url(r'^$', newLocation),
    url(r'^$', locationEdit, name='location-edit'),
    url(r'^suggestions', suggestions, name='suggestions'),
    url(r'^create-location$', get_or_create_location, name="get_or_create_location"),
    url(r'^update-location$', update_location, name="update_location"),
    url(r'^location-contents/(?P<location_id>[0-9]+)', location_contents, name="location-contents"),
    url(r'^json/', cardListJSON),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
