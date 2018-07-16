
from django.contrib import admin
from django.urls import path
from django.conf.urls import  url
from . import views
app_name='app'
urlpatterns = [
    url(r'^$', views.index ,name='index'),
    url(r'^data/(?P<id>[0-9]+)$', views.data ,name='data'),
    url(r'^timeline/', views.timeline ,name='timeline'),
    url(r'^timeline_details/(?P<id>[0-9]+)$', views.timeline_details ,name='timeline_details'),
    url(r'^posts/(?P<id>[0-9]+)$',views.show,name='show'),
    path('admin/', admin.site.urls),
]
