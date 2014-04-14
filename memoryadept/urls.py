from django.conf.urls import patterns, include, url
from django.contrib import admin

from main.views import newLocation, locationList, locationEdit, cardListJSON

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'memoryadept.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', newLocation),
    url(r'^locations$', locationList, name='location-list'),
    url(r'^location/(?P<location_id>\n+)$', locationEdit, name='location-edit'),
    url(r'^json$', cardListJSON),
    url(r'^admin/', include(admin.site.urls)),
)
