from src.rooms.models import Room


class RoomRepository:
    @staticmethod
    def create_room(description: str, price: float) -> Room:
        return Room.objects.create(description=description, price_per_night=price)

    @staticmethod
    def delete_room(room_id: int) -> None:
        Room.objects.filter(id=room_id).delete()

    @staticmethod
    def get_rooms(order_by: str = "id", ascending: bool = True):
        if order_by not in ["price", "created_at"]:
            order_by = "created_at"
        if not ascending:
            order_by = "-" + order_by
        return Room.objects().all().order_by(order_by)
