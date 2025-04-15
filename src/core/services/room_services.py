from src.core.repositories.room_repository import RoomRepository


class RoomServices:
    @staticmethod
    def create_room(description: str, price: float) -> int:
        room = RoomRepository.create_room(description, price)
        return room

    @staticmethod
    def delete_room(room_id: int) -> None:
        RoomRepository.delete_room(room_id)

    @staticmethod
    def list_rooms(order_by: str = "created_at", ascending: bool = True) -> list:
        return RoomRepository.get_rooms(order_by=order_by, ascending=ascending)
