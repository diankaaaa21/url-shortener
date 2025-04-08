import pytest
from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient

from shortener_api.models import ShortURL

pytestmark = pytest.mark.django_db


def test_create_short_url_web_view_get():
    client = Client()
    response = client.get(reverse("create-url-form"))
    assert response.status_code == 200
    assert "text/html" in response["Content-Type"]


def test_create_short_url_web_view_post_valid():
    client = Client()
    response = client.post(
        reverse("create-url-form"), {"original_url": "https://example.com"}
    )
    assert response.status_code == 302
    assert ShortURL.objects.filter(original_url="https://example.com").exists()


def test_create_short_url_web_view_post_invalid():
    client = Client()
    response = client.post(reverse("create-url-form"), {"original_url": "не_ссылка"})
    assert response.status_code == 200
    assert "Введите" in response.content.decode()


def test_redirect_to_original_view():
    obj = ShortURL.objects.create(original_url="https://google.com", token="abc123")
    client = Client()
    response = client.get(reverse("redirect-to-original", args=[obj.token]))
    assert response.status_code == 302
    assert response.url == obj.original_url

    obj.refresh_from_db()
    assert obj.click_count == 1


def test_create_short_url_api_valid():
    client = APIClient()
    response = client.post(
        reverse("create-url-api"), {"original_url": "https://test.com"}, format="json"
    )
    assert response.status_code == 201
    data = response.json()
    assert "short_url" in data
    assert ShortURL.objects.filter(original_url="https://test.com").exists()


def test_create_short_url_api_invalid_url():
    client = APIClient()
    response = client.post(
        reverse("create-url-api"), {"original_url": "not-a-url"}, format="json"
    )
    assert response.status_code == 400
    assert "original_url" in response.json()
