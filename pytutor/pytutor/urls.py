from django.conf.urls import patterns, include, url

# from tutor import urls as tutor_urls


urlpatterns = patterns('',
    #BASE URL MAPPINGS
    url(r'^$', 'pytutor.views.home'),

    # TUTOR URL MAPPINGS
    # --------------------------------- STUDYING
    url(r'^tutor$', 'tutor.views.study'),
    url(r'^tutor/(?P<pk>[0-9]?)/respond[/]$', 'tutor.views.respond'),

    # --------------------------------- EDITING
    url(r'^tutor/list', 'tutor.views.list'),
    url(r'^tutor/new', 'tutor.views.question_form'),
    url(r'^tutor/(?P<pk>[0-9]?)/edit[/]$', 'tutor.views.question_form'),
    url(r'^tutor/save', 'tutor.views.save_question'),
    url(r'^tutor/test/save', 'tutor.views.add_test'),
    url(r'^tutor/test/(?P<pk>[0-9]?)/del', 'tutor.views.del_test'),

    # --------------------------------- USERS
    url(r'^login$', 'tutor.user_views.user_login'),
    url(r'^logout$', 'tutor.user_views.user_logout'),
    url(r'^login-sorry$', 'tutor.user_views.login_error'),
    url(r'^register$', 'tutor.user_views.register'),

)
