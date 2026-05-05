from rest_framework import serializers


class DiabeticFootUlcerPredictionSerializer(serializers.Serializer):
    prediction = serializers.IntegerField()
    label = serializers.CharField()
    confidence = serializers.FloatField(required=False)
    scores = serializers.DictField(child=serializers.FloatField(), required=False)
