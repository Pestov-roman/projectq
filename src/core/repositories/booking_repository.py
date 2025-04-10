from rooms.models import Booking
from django.db.models import Q
from datetime import date


def create_booking(room_id: int, date_start: date, date_end: date) -> Booking:
    return Booking.objects.create(
        room_id=room_id, date_start=date_start, date_end=date_end
    )


def delete_booking(booking_id: int) -> None:
    Booking.objects.filter(id=booking_id).delete()


def list_bookings_by_room(room_id: int) -> list:
    return Booking.objects().filter(room_id=room_id).order_by("date_start")


def get_booking_by_id(booking_id: int) -> Booking:
    return Booking.objects.filter(id=booking_id)


def is_available(room_id: int, start: date, end: date) -> bool:
    return (
        Booking.objects.filter(room_id=room_id)
        .filter(Q(date_start__lte=end) & Q(date_end__gte=start))
        .exists()
    )
