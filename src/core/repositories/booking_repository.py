from src.core.models import Room
from datetime import date
from src.bookings.models import Booking
from typing import Optional


class BookingRepository:
    @staticmethod
    def create_booking(room_id: int, check_in: date, check_out: date) -> Booking:
        return Booking.objects.create(
            room_id=room_id, check_in=check_in, check_out=check_out
        )

    @staticmethod
    def delete_booking(booking_id: int) -> None:
        Booking.objects.filter(id=booking_id).delete()

    @staticmethod
    def get_bookings_by_room(room_id: int) -> list[Booking]:
        return Booking.objects.filter(room_id=room_id).order_by("check_in")

    @staticmethod
    def is_available(room_id: int, check_in: date, check_out: date) -> bool:
        overlapping_bookings = Booking.objects.filter(
            room_id=room_id,
            check_in__lt=check_out,
            check_out__gt=check_in,
        ).exists()
        return not overlapping_bookings

    @staticmethod
    def get_booking_by_id(booking_id: int) -> Optional[Booking]:
        try:
            return Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return None
