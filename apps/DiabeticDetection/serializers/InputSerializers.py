from rest_framework import serializers


class DiabeticFootUlcerImageSerializer(serializers.Serializer):
    image = serializers.ImageField(
        help_text="Foot image (JPEG/PNG). Resized to 224×224 RGB as in training.",
    )
