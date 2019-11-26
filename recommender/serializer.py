from rest_framework import serializers
from recommender.models import Result


class ResultSerializer(serializers.ModelSerializer):
    target = serializers.CharField()
    class Meta:
        model = Result
        fields = ('target',)
