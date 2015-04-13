from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles import views


from social.views import SocialView, ConnectionView


urlpatterns = patterns('',
    #BASE URL MAPPINGS
    url(r'^$', 'pytutor.views.home'),

    # User URL MAPPINGS
    url(r'^study/report$', 'tutor.student_views.report'),
    url(r'^study/report/(?P<user_name>.*)[/]$', 'tutor.student_views.report'),
    url(r'^study/question_detail/([0-9]+?)[/]$', 'tutor.student_views.question_detail'),
    #no idea ^

    # TUTOR URL MAPPINGS
    # --------------------------------- STUDYING
    url(r'^tutor$', 'tutor.study_views.study'),
    url(r'^tutor/(?P<sticky_id>[0-9]+?)[/]$', 'tutor.study_views.study'),
    url(r'^tutor/tag/(?P<study_tag>.*)[/]$', 'tutor.study_views.study'),
    # url(r'^tutor/(?P<sticky_id>[0-9]+?)/tag/(?P<study_tag>.*)[/]$', 'tutor.study_views.study'),
    url(r'^tutor/(?P<pk>[0-9]+?)/respond[/]$', 'tutor.study_views.study'),
    url(r'^tutor/([0-9]+?)/solutions[/]$', 'tutor.study_views.solutions'),
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

    # --------------------------------- USER PROFILE
    url(r'^~(.*)[/]$', 'social.views.public'),
    url(r'^profile[/]$', 'social.views.profile'),
    url(r'^api/profile[/]$', SocialView.as_view()),
    url(r'^api/friend/find[/]$', 'social.views.find_friends'),
    url(r'^api/profile/pic[/]$', 'social.views.post_profile_pic'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)