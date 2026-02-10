# studycalender/config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from .views import RootView, APIRootView


# --------------------------------------------------
# API DOCUMENTATION
# --------------------------------------------------
docs_urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

# --------------------------------------------------
# URL PATTERNS
# --------------------------------------------------
urlpatterns = [
    # Root
    path("", RootView.as_view(), name="root"),

    # API Root
    path("api/", APIRootView.as_view(), name="api-root"),

    # Admin
    path("admin/", admin.site.urls),

    # ---------------------------
    # API - Apps
    # ---------------------------
    path("api/users/", include("apps.users.urls")),
    path("api/calendars/", include("apps.calendars.urls")),
    path("api/study/", include("apps.study.urls")),
    path("api/reports/", include("apps.reports.urls")),

    # ---------------------------
    # Browsable API (Session Auth)
    # ---------------------------
    path("api/auth-session/", include("rest_framework.urls")),
]

# API Docs
urlpatterns += docs_urlpatterns

# Media (DEV only)
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
