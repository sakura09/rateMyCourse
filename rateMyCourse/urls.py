from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    #GET
    url(r'^$', views.getIndex, name='getIndex'),
    url(r'^index/$', views.getIndex, name='getIndex'),
    url(r'^search/$', views.searchSchool, name='searchSchool'),
    url(r'^course/(?P<course_number>[0-9A-Z]+)/$', views.coursePage, name='getCourse'),

    #POST
    url(r'^signIn/$', views.signIn, name='signIn'),
    url(r'^signUp/$', views.signUp, name='signUp'),
    url(r'^course_addComment/$', views.courseAddComment, name='courseAddComment'),
    url(r'^course_addRate/$', views.courseAddRate, name='courseAddRate'),

    #TMP GET IN INDEX
    url(r'^getSchool/$', views.getSchool, name='getSchool'),
    url(r'^getDepartment/$', views.getDepartment, name='getDepartment'),
    url(r'^getCourse/$', views.getCourse, name='getCourse'),
]
