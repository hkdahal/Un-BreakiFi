from rest_framework import serializers

from SystemApp import models

from SystemApp.manual_features import tell_features


class UserSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField('provide_features')

    def provide_features(self, user):
        return tell_features(user.auth_id)

    class Meta:
        fields = (
            'auth_id', 'features'
        )
        model = models.Individual


