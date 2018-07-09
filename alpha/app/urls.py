
from django.contrib import admin
from django.urls import path
from django.conf.urls import  url
from . import views
app_name='app'
urlpatterns = [
    url(r'^$', views.index ,name='index'),
    url(r'^data/', views.data ,name='data'),
    url(r'^posts/(?P<id>[0-9]+)$',views.show,name='show'),
    path('admin/', admin.site.urls),
]
