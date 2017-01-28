from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^vendors/$', views.vendors),
    url(r'^vendors/expense$', views.vendors),
]
