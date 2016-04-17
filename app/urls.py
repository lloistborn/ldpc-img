from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^encode$', views.encode, name='encode'),
	url(r'^decode$', views.decode, name='decode')
]
