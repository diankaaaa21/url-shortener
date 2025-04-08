import pytest

from shortener.models import ShortURL


@pytest.mark.django_db
def test_create_short_url(client):
    response = client.post("/", {"original_url": "https://google.com"})
    assert response.status_code == 302
    obj = ShortURL.objects.first()
    assert obj.original_url == "https://google.com"


@pytest.mark.django_db
def test_redirect_to_original(client):
    obj = ShortURL.objects.create(original_url="https://test.com", token="abc123")
    response = client.get(f"/{obj.token}/")
    assert response.status_code == 302
    assert response.url == "https://test.com"


@pytest.mark.django_db
def test_stats_view(client):
    response = client.get("/stats/")
    assert response.status_code == 200
