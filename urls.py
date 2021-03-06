from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout
import lernado.views as views
import lernado.accounts.views as account_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^$', views.home),
    ('^courses/$', views.courses),
    ('^accounts/login/$', login),
    ('^accounts/logout/$', logout),
    ('^accounts/(?P<user_id>\d+)/pic/$', account_views.profile_pic),
    ('^accounts/(?P<user_id>\d+)/profile/$', account_views.view_profile),
    ('^accounts/(?P<user_id>\d+)/editprofile/$', account_views.edit_profile),
    (r'^course/(?P<course_id>\d+)/$', views.course),
    (r'^course/enroll/(?P<course_id>\d+)/$', views.enroll),
    (r'^course/drop/(?P<course_id>\d+)/$', views.drop_course),
    (r'^course/(?P<course_id>\d+)/participants/$', views.course_participants),
    (r'^course/(?P<course_id>\d+)/activityresponses/$', views.all_activity_submissions),
    (r'^course/(?P<course_id>\d+)/page/(?P<page_id>\d+)/$', views.course_page),
    (r'^course/(?P<course_id>\d+)/question/(?P<question_id>\d+)/$', views.question),
    (r'^course/(?P<course_id>\d+)/question/(?P<question_id>\d+)/edit/$', views.edit_question),
    (r'^course/(?P<course_id>\d+)/question/(?P<question_id>\d+)/like/$', views.like_question),
    (r'^course/(?P<course_id>\d+)/question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/edit/$', views.edit_answer),    
    (r'^course/(?P<course_id>\d+)/question/(?P<question_id>\d+)/answer/(?P<answer_id>\d+)/like/$', views.like_answer),
    (r'^course/(?P<course_id>\d+)/askquestion/$', views.ask_question),
    (r'^course/(?P<course_id>\d+)/activity/(?P<activity_id>\d+)/$', views.activity),
    (r'^course/(?P<course_id>\d+)/activity/(?P<activity_id>\d+)/response/(?P<activity_response_id>\d+)/$', views.activity_response),
    (r'^course/(?P<course_id>\d+)/activity/(?P<activity_id>\d+)/response/(?P<activity_response_id>\d+)/edit/$', views.edit_activity_response),
    (r'^course/(?P<course_id>\d+)/activity/(?P<activity_id>\d+)/response/(?P<activity_response_id>\d+)/review/(?P<activity_response_review_id>\d+)/edit/$', views.edit_activity_response_review),    
    (r'^page/(?P<page>.+)/$', views.page),
    # Examples:
    # url(r'^$', 'lernado.views.home', name='home'),
    # url(r'^lernado/', include('lernado.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'password/done/$', 'django.contrib.auth.views.password_change_done'),
    (r'^password/change/$','django.contrib.auth.views.password_change'),
    (r'^password/reset/$','django.contrib.auth.views.password_reset'),
    (r'^password/reset/done/$','django.contrib.auth.views.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name' : 'registration/password_reset.html',  'post_reset_redirect': '/accounts/logout/' }),
    url(r'^admin/', include(admin.site.urls)),
    
)
