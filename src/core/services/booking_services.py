from datetime import date
from django.core.exceptions import ValidationError
from src.core.repositories.booking_repository import BookingRepository


class BookingService:
    @staticmethod
    def create_booking(room_id: int, date_start: date, date_end: date):
        if not BookingRepository.is_available(room_id, date_start, date_end):
            raise ValidationError("Комната забронирована на эти даты")
        return BookingRepository.create_booking(room_id, date_start, date_end)

    @staticmethod
    def delete_booking(booking_id: int) -> None:
        BookingRepository.delete_booking(booking_id)

    @staticmethod
    def list_bookings_for_room(room_id: int) -> list:
        return BookingRepository.get_bookings_by_room(room_id)
