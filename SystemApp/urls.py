from django.conf.urls import url
from . import views, manual_features

urlpatterns = [
    url(r'^$', views.index),
    url(r'^user-(?P<user_id>\d+)/vendors/expense$', views.vendors_vs_expense),
    url(r'^user-(?P<user_id>\d+)/vendors/transactions',
        views.vendors_vs_transactions),
    url(r'^user-(?P<user_id>\d+)/dates', views.per_date),
    url(r'^user-(?P<user_id>\d+)/transport', views.transportation),
    url(r'^user-(?P<user_id>\d+)/vendors', views.vendor_lst),
    url(r'^user-(?P<user_id>\d+)/vendor/(?P<vendor_id>\d+)$',
        views.vendor_transactions),
    url(r'^user-(?P<user_id>\d+)/profile$', manual_features.provide_profile),
    url(r'^user-(?P<user_id>\d+)/activities/(?P<d>.*)/$',
        views.day_specific_transactions),
    url(r'^user-(?P<user_id>\d+)/ie', views.monthly_expense_income),
    url(r'^user-(?P<user_id>\d+)/housing', views.housing_expense),
    url(r'^user-(?P<user_id>\d+)/foods', views.restaurant_info),
    url(r'^add-user', views.add_user),


]
