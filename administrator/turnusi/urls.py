from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

from django.views.generic import TemplateView

from . import views

urlpatterns = [
	url(r'^$', views.get_turnusi, name="get_turnusi"),
	url(r'^(?P<turnus_id>\d+)/$', views.turnus, name="turnus"),
	url(r'^(?:(?P<turnus_id>\d+)/)?turnus_add/$', views.turnus_add, name="turnus_add"),
	url(r'^(?P<turnus_id>\d+)/turnus_remove/$', views.turnus_remove, name="turnus_remove"),
	url(r'^(?P<turnus_id>\d+)/shift_manage/$', views.turnusi_shift_manage, name="turnusi_shift_manage"),
	url(r'^(?P<turnus_id>\d+)/shift_remove/$', views.turnusi_shift_remove, name="turnusi_shift_remove"),
]

