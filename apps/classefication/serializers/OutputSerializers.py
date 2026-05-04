from rest_framework import serializers


class DiabetesPredictionOutputSerializer(serializers.Serializer):
    prediction = serializers.IntegerField()
    label = serializers.CharField()
    probability = serializers.FloatField(required=False)
