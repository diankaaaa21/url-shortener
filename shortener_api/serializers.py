from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from rest_framework import serializers


class ShortURLSerializer(serializers.Serializer):
    original_url = serializers.CharField()

    def validate_original_url(self, value):
        validator = URLValidator(schemes=["http", "https"])
        try:
            validator(value)
        except ValidationError:
            raise serializers.ValidationError(
                "Введите корректный URL (http или https)."
            )
        return value
