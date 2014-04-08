from django.conf.urls import patterns, include, url

from django.contrib import admin

from main.views import newLocation

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'memoryadept.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'', newLocation),

    url(r'^admin/', include(admin.site.urls)),
)
