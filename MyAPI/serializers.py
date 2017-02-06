from rest_framework import serializers

from SystemApp import models

from SystemApp.manual_features import tell_features


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('user', 'id')
        model = models.Features


