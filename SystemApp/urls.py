from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user-(?P<user_id>\d+)/vendors/expense$', views.vendors_vs_expense),
    url(r'^user-(?P<user_id>\d+)/vendors/transactions', views.vendors_vs_transactions),
    url(r'^user-(?P<user_id>\d+)/dates', views.per_date),
    url(r'^user-(?P<user_id>\d+)/transport', views.transportation),
    url(r'^user-(?P<user_id>\d+)/income', views.income_vs_expense),
    url(r'^user-(?P<user_id>\d+)/vendors', views.vendor_lst),
    url(r'^user-(?P<user_id>\d+)/vendor/(?P<vendor_id>\d+)$', views.vendor_transactions),

]
