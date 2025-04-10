from rooms.models import Room
from django.db.models import Q


def create_room(description: str, price: float) -> Room:
    return Room.objects.create(description=description, price_per_night=price)


def delete_room(room_id: int) -> None:
    Room.objects.filter(id=room_id).delete()


def list_rooms(order_by="created_at", ascending=True) -> list:
    return Room.objects().all().order_by(order_by)


def get_room_by_id(room_id: int) -> Room:
    return Room.objects.get(id=room_id)
