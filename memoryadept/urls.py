from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve as serve_static
from django.contrib import admin

from main.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'memoryadept.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', newLocation),
    #url(r'^locations$', locationList, name='location-list'),
    url(r'^locations$', locationEdit, name='location-edit'),
    url(r'^create-location$', get_or_create_location, name="get_or_create_location"),
    url(r'^location-contents/(?P<location_id>[0-9]+)', location_contents, name="location-contents"),
    url(r'^json/', cardListJSON),
    url(r'^admin/', include(admin.site.urls)),
)# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns += staticfiles_urlpatterns()

urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
