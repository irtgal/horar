from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from . import views

urlpatterns = [	
	url(r'^prijava/$', views.login_user, name="login_user"),
	url(r'^uporabnik/$', views.profile, name="profile"),
	url(r'^odjava/$', views.logout_user, name="logout_user"),
	
	url(r'^(?P<group_id>\d+)/$', views.group_index, name="group_index"),
	url(r'^(?P<group_id>\d+)/message_add/$', views.message_add, name="message_add"),

	url(r'^(?P<group_id>\d+)/urnik/$', views.timetable_index, name="timetable_index"),
	url(r'^(?P<group_id>\d+)/urnik/dodaj/$', views.add, name="add"),
	url(r'^(?P<group_id>\d+)/urnik/check/$', views.timetable_check, name="timetable_check"),
	url(r'^(?P<group_id>\d+)/(?P<shift_id>\d+)/$', views.get_status, name="get_status"),

	url(r'^(?P<group_id>\d+)/urnik/absent/$', views.absent, name="absent"),
	url(r'^(?P<group_id>\d+)/urnik/absent/(?P<date>\d{4}-\d{2}-\d{2})/$', views.get_absent, name="get_absent"),
	
	url(r'^(?P<group_id>\d+)/urnik/note_change/$', views.note_change, name="note_change"),


]
