from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import re_path

admin.autodiscover()

urlpatterns = [
    re_path("^admin/", admin.site.urls),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
