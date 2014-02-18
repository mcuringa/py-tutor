# tutor.urls.py
# by: mxc
"""
Define the mappings for URLs in
the tutor app.
"""

from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.list),
    url(r'^new$', views.quest_form),
    url(r'^(?P<pk>[0-9]?)[/]$', views.app_form),
    url(r'^([0-9]?)/del[/]$', views.del_app),
    url(r'^save_app$', views.save_app),
)

