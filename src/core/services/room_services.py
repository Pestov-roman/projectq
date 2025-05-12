from src.core.repositories.room_repository import RoomRepository
from src.core.models import Room


class RoomServices:
    @staticmethod
    def create_room(
        description: str, price_per_night: float, capacity: int, number: str
    ) -> Room:
        room = RoomRepository.create_room(
            description, price_per_night, capacity, number
        )
        return room

    @staticmethod
    def delete_room(room_id: int) -> None:
        RoomRepository.delete_room(room_id)

    @staticmethod
    def list_rooms(order_by: str = "created_at", ascending: bool = True) -> list:
        return RoomRepository.get_rooms(order_by=order_by, ascending=ascending)
