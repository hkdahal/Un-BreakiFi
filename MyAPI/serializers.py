from rest_framework import serializers

from SystemApp import models

import SystemApp.manual_features as feature


class UserSerializer(serializers.ModelSerializer):
    # song_set = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    features = serializers.SerializerMethodField('tell_features')

    def tell_features(self, user):
        the_features = dict()
        user_id = user.auth_id
        the_features['student'] = feature.is_student(user_id)
        the_features['has_kids'] = feature.has_kids(user_id)
        the_features['student_loan'] = feature.has_been_paying_student_loans(user_id)
        the_features['pets'] = feature.has_pets(user_id)
        the_features['an_artist'] = feature.is_an_artist(user_id)
        the_features['moved'] = feature.is_moving(user_id)
        the_features['peaceful'] = feature.likes_peace(user_id)
        the_features['purposing'] = feature.is_purposing(user_id)
        the_features['athletic'] = feature.is_athletic(user_id)
        the_features['divorced'] = feature.is_divorced(user_id)
        the_features['outgoing'] = feature.is_outgoing(user_id)
        the_features['figurine_stuffs'] = feature.is_into_stuffs(user_id)

        return the_features

    class Meta:
        fields = (
            'auth_id', 'features'
        )
        model = models.Individual


