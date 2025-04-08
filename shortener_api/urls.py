from django.urls import path

from .views import CreateShortURLAPIView, ShortURLStatsAPIView, redirect_to_original

urlpatterns = [
    path("", CreateShortURLAPIView.as_view(), name="create_url"),
    path("stats/", ShortURLStatsAPIView.as_view(), name="url_stats"),
    path("<str:token>/", redirect_to_original, name="redirect"),
]
