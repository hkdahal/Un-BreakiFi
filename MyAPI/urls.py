from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^users',
        views.ListUser.as_view(),
        name='users_and_features'
        ),

    url(r'^user-(?P<auth_id>\d+)/$',
        views.RetrieveUpdateDestroyUser.as_view(),
        name="specific user details"
        ),
]
