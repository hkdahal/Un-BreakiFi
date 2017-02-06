from rest_framework import generics
from django.shortcuts import get_object_or_404


from SystemApp import models
from . import serializers


class ListUser(generics.ListAPIView):
    queryset = models.Features.objects.all()
    serializer_class = serializers.UserSerializer


class RetrieveUpdateDestroyUser(generics.RetrieveUpdateDestroyAPIView):
    # lookup_field = 'auth_id'
    queryset = models.Features.objects.all()
    serializer_class = serializers.UserSerializer

    # def get_queryset(self):
    #     auth_id = self.kwargs.get('auth_id')
    #     if auth_id:
    #         return self.queryset.filter(user__auth_id=auth_id)

    def get_object(self):
        auth_id = self.kwargs.get('auth_id')
        return get_object_or_404(
            self.queryset,
            user__auth_id=auth_id
        )
