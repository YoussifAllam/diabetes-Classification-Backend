from rest_framework import serializers


class DiabetesPredictionInputSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=["male", "female", "other"])
    age = serializers.FloatField(min_value=0)
    hypertension = serializers.IntegerField(min_value=0, max_value=1)
    heart_disease = serializers.IntegerField(min_value=0, max_value=1)
    smoking_history = serializers.ChoiceField(
        choices=["never", "no info", "current", "former", "ever", "not current"]
    )
    bmi = serializers.FloatField(min_value=0)
    HbA1c_level = serializers.FloatField(min_value=0)
    blood_glucose_level = serializers.FloatField(min_value=0)
