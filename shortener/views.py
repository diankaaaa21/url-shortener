from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.views import APIView

from .models import ShortURL
from .tasks import log_url_creation


class CreateShortURLAPIView(APIView):
    def get(self, request):
        return render(request, "shortener/create.html")

    def post(self, request):
        original_url = request.POST.get("original_url")
        if original_url:
            obj, _ = ShortURL.objects.get_or_create(original_url=original_url)
            log_url_creation.delay(obj.original_url, obj.token)
            return redirect(f"/{obj.token}")
        return render(request, "shortener/create.html", {"error": "Введите ссылку!"})


class ShortURLStatsAPIView(APIView):
    def get(self, request):
        urls = ShortURL.objects.order_by("-click_count")
        return render(request, "shortener/stats.html", {"urls": urls})


def redirect_to_original(request, token):
    obj = get_object_or_404(ShortURL, token=token)
    obj.click_count += 1
    obj.save(update_fields=["click_count"])
    return redirect(obj.original_url)
