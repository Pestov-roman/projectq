from django.urls import path
from .views import RoomCreateView, RoomDeleteView, RoomListView

urlpatterns = [
    path("create", RoomCreateView.as_view(), name="room-create"),
    path("delete", RoomDeleteView.as_view(), name="room-delete"),
    path("list", RoomListView.as_view(), name="room-list"),
]
