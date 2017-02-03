from rest_framework import generics


from SystemApp import models
from . import serializers


class ListCreateUser(generics.ListCreateAPIView):
    queryset = models.Individual.objects.all()
    serializer_class = serializers.UserSerializer
