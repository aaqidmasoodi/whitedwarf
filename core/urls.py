from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from django.contrib import admin
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="CUKBRS API",
        default_version="v1",
        description="Official API for CUK Bus Reservation System",
        terms_of_service="https://www.cukashmir.ac.in/",
        contact=openapi.Contact(email="contact@cukashmir.ac.in"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]


admin.site.site_header = "CUK Bus Reservation System"
admin.site.index_title = "Administration"
