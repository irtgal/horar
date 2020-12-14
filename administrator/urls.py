from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from django.views.generic import TemplateView

from . import views

urlpatterns = [
	url(r'^(?P<group_id>\d+)/$', views.group, name="group"),
	url(r'^(?P<group_id>\d+)/urnik/$', views.timetable_administrator, name="timetable_administrator"),

	url(r'^(?P<group_id>\d+)/urnik/dodaj$', views.timetable_add, name="timetable_add"),
	url(r'^(?P<group_id>\d+)/urnik/check/$', views.timetable_check, name="timetable_check"),
	url(r'^(?P<group_id>\d+)/user_remove$', views.user_remove, name="user_remove"),
	url(r'^(?P<group_id>\d+)/user_add$', views.user_add, name="user_add"),

	url(r'^(?P<group_id>\d+)/urnik/shift_manage/$', views.shift_manage, name="shift_manage"),
	url(r'^(?P<group_id>\d+)/urnik/shift_remove/$', views.shift_remove, name="shift_remove"),

	url(r'^(?P<group_id>\d+)/turnusi/', include('administrator.turnusi.urls')),
]

