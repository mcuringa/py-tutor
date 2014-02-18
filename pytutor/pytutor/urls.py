from django.conf.urls import patterns, include, url

# from tutor import urls as tutor_urls


urlpatterns = patterns('',
    #BASE URL MAPPINGS
    url(r'^$', 'pytutor.views.home'),

    # TUTOR URL MAPPINGS
    # --------------------------------- STUDYING
    url(r'^tutor$', 'tutor.views.study'),

    # --------------------------------- EDITING
    url(r'^tutor/list', 'tutor.views.list'),
    url(r'^tutor/new', 'tutor.views.new_question'),
    url(r'^tutor/(?P<pk>[0-9]?)/edit[/]$', 'tutor.views.new_question'),
    url(r'^tutor/save', 'tutor.views.save_question'),

)
