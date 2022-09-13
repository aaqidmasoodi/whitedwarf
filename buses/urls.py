from django.urls import path
from . import views


urlpatterns = [
    path("", views.BusListView.as_view(), name="buses"),
    path("allocate/", views.BusAllocateView.as_view(), name="allocate-bus"),
    path("members/", views.BusMembersListView.as_view(), name="members"),
]
