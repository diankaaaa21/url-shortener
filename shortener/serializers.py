from rest_framework import serializers

from .models import ShortURL


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ["original_url", "token", "click_count", "created_at"]
        read_only_fields = ["token", "click_count", "created_at"]
