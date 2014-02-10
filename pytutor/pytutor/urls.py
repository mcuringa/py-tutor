from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import tutor


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pytutor.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url('^tutor/', include(tutor.urls)),
)
