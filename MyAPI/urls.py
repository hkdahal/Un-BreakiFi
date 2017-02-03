from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^users', views.ListCreateUser.as_view(), name='user_list'),

]
