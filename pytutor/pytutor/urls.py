from django.conf.urls import patterns, include, url

# from tutor import urls as tutor_urls


urlpatterns = patterns('',
    #BASE URL MAPPINGS
    url(r'^$', 'pytutor.views.home'),

    # User URL MAPPINGS
    url(r'^study/report$', 'tutor.student_views.report'),

    # TUTOR URL MAPPINGS
    # --------------------------------- STUDYING
    url(r'^tutor$', 'tutor.study_views.study'),
    url(r'^tutor/(?P<try_again_id>[0-9]+?)[/]$', 'tutor.study_views.study'),
    url(r'^tutor/tag/(?P<study_tag>.*)[/]$', 'tutor.study_views.study'),
    url(r'^tutor/(?P<try_again_id>[0-9]+?)/tag/(?P<study_tag>.*)[/]$', 'tutor.study_views.study'),
    url(r'^tutor/(?P<pk>[0-9]+?)/respond[/]$', 'tutor.study_views.study'),
    url(r'^tutor/tags', 'tutor.study_views.tags'),
    # url(r'^tutor/no_questions$', 'tutor.study_views.no_questions'),
    url(r'^tutor/response/submit', 'tutor.study_views.respond'),



    # --------------------------------- EDITING
    url(r'^question/list/(?P<editor_name>.*)[/]$', 'tutor.editor_views.list'),
    url(r'^question/list[/]$', 'tutor.editor_views.list'),
    url(r'^question/(?P<pk>[0-9]+?)/dup[/]$', 'tutor.editor_views.dup'),
    url(r'^question/new', 'tutor.editor_views.question_form'),
    url(r'^question/(?P<pk>[0-9]+?)/edit[/]$', 'tutor.editor_views.question_form'),
    url(r'^question/(?P<pk>[0-9]+?)/delete[/]$', 'tutor.editor_views.delete_question'),
    url(r'^question/save', 'tutor.editor_views.save_question'),
    url(r'^question/(?P<pk>[0-9]+?)/diff/(?P<v1>[0-9]+?),(?P<v2>[0-9]+?)[/]$', 'tutor.editor_views.diff'),
    url(r'^question/(\d+)/revert/(\d+)[/]$', 'tutor.editor_views.revert'),
    url(r'^question/test/save', 'tutor.editor_views.add_test'),
    url(r'^question/test/(?P<pk>[0-9]+?)/del', 'tutor.editor_views.del_test'),



    # --------------------------------- USERS
    url(r'^login$', 'tutor.user_views.user_login'),
    url(r'^logout$', 'tutor.user_views.user_logout'),
    url(r'^login-sorry$', 'tutor.user_views.login_error'),
    url(r'^register$', 'tutor.user_views.register'),

)
