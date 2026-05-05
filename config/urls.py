from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

third_party_urls = [
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("site_administration/", admin.site.urls),
]

urlpatterns = [
    path("api/", lambda request: HttpResponse("API OK")),
    path("api/classification/", include("apps.classefication.urls")),
    path("api/diabetic-detection/", include("apps.DiabeticDetection.urls")),
    # Health check endpoint
    path("health/", lambda request: HttpResponse("OK")),
] + third_party_urls  # noqa
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
