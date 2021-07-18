from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from .views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    
    
    url('administrator/', include('administrator.urls')),
    url('urniki/', include('timetables.urls')),
    url(r'^$', home, name="home"),
	url(r'^doma/', home, name="home"),
]
