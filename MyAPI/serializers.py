from rest_framework import serializers

from SystemApp import models

from SystemApp.manual_features import is_student


class UserSerializer(serializers.ModelSerializer):
    # song_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    student = serializers.SerializerMethodField('say_hello')

    def say_hello(self, user):
        return is_student(user.auth_id)

    class Meta:
        fields = (
            'auth_id', 'student'
        )
        model = models.Individual


class VendorSerializer(serializers.ModelSerializer):
    # song_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        fields = (
            'store_name'
        )
        model = models.Vendor

