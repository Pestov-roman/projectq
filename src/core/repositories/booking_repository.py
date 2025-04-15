from src.rooms.models import Room
from datetime import date
from src.bookings.models import Booking
from typing import Optional


class BookingRepository:
    @staticmethod
    def create_booking(room_id: int, date_start: date, date_end: date) -> Booking:
        return Booking.objects.create(
            room_id=room_id, date_start=date_start, date_end=date_end
        )

    @staticmethod
    def delete_booking(booking_id: int) -> None:
        Booking.objects.filter(id=booking_id).delete()

    @staticmethod
    def get_bookings_by_room(room_id: int) -> list[Booking]:
        return Booking.objects.filter(room_id=room_id).order_by("date_start")

    @staticmethod
    def is_available(room_id: int, date_start: date, date_end: date) -> bool:
        overlapping_bookings = Booking.objects.filter(
            room_id=room_id,
            date_start__lt=date_end,
            date_end__gt=date_start,
        ).exists()
        return not overlapping_bookings

    @staticmethod
    def get_booking_by_id(booking_id: int) -> Optional[Booking]:
        try:
            return Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return None
