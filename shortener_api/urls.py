from django.urls import path

from .views import (
    CreateShortURLAPIView,
    CreateShortURLWebView,
    ShortURLStatsWebView,
    redirect_to_original,
)

urlpatterns = [
    path("create/", CreateShortURLWebView.as_view(), name="create-url-form"),
    path("api/create/", CreateShortURLAPIView.as_view(), name="create-url-api"),
    path("stats/", ShortURLStatsWebView.as_view(), name="url-stats"),
    path("<str:token>/", redirect_to_original, name="redirect-to-original"),
]
