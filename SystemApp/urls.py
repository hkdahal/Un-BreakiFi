from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^vendors/expense$', views.vendors_vs_expense),
    url(r'^vendors/transactions', views.vendors_vs_transactions),
    url(r'^dates', views.per_date),


]
