from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import TemplateView
from chatapi.views import generate_image_view, get_history

urlpatterns = [
    path("api/generate-image/", generate_image_view),
    path("api/history/", get_history),
    path("", TemplateView.as_view(template_name="index.html")),
]

# ✅ Add this at the bottom of the file
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
