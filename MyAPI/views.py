from rest_framework import generics


from SystemApp import models
from . import serializers


class ListUser(generics.ListAPIView):
    queryset = models.Individual.objects.all()
    serializer_class = serializers.UserSerializer


class RetrieveUpdateDestroyUser(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'auth_id'
    queryset = models.Individual.objects.all()
    serializer_class = serializers.UserSerializer
