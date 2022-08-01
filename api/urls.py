from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.APIHome.as_view(), name="api-home"),
    path("accounts/", include("accounts.urls")),
    path("payments/", include("payments.urls")),
]
