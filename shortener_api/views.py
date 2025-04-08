from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortURL
from .serializers import ShortURLSerializer
from .tasks import log_url_creation
from .throttling import CreateShortURLThrottle


class CreateShortURLWebView(View):
    def get(self, request):
        return render(request, "shortener_api/create.html")

    def post(self, request):
        original_url = request.POST.get("original_url")
        validator = URLValidator(schemes=["http", "https"])

        try:
            validator(original_url)
        except ValidationError:
            return render(
                request,
                "shortener_api/create.html",
                {"error": "Введите корректный URL!"},
            )

        obj, _ = ShortURL.objects.get_or_create(original_url=original_url)
        log_url_creation.delay(obj.original_url, obj.token)
        return redirect("redirect-to-original", token=obj.token)


class CreateShortURLAPIView(APIView):
    throttle_classes = [CreateShortURLThrottle]

    def post(self, request):
        serializer = ShortURLSerializer(data=request.data)
        if serializer.is_valid():
            original_url = serializer.validated_data["original_url"]
            obj, _ = ShortURL.objects.get_or_create(original_url=original_url)
            log_url_creation.delay(obj.original_url, obj.token)
            return Response(
                {"short_url": f"/{obj.token}"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShortURLStatsWebView(View):
    def get(self, request):
        urls = ShortURL.objects.order_by("-click_count")
        return render(request, "shortener_api/stats.html", {"urls": urls})


def redirect_to_original(request, token):
    obj = get_object_or_404(ShortURL, token=token)
    obj.click_count += 1
    obj.save(update_fields=["click_count"])
    return redirect(obj.original_url)
