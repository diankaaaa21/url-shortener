import random
import string

from django.db import models


def generate_token():
    chars = string.ascii_letters + string.digits
    while True:
        token = "".join(random.choices(chars, k=6))
        if not ShortURL.objects.filter(token=token).exists():
            return token


class ShortURL(models.Model):
    original_url = models.URLField()
    token = models.CharField(max_length=6, unique=True, default=generate_token)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.token} - {self.original_url}"
