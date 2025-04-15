from datetime import date
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from src.core.repositories.booking_repository import BookingRepository
from src.core.models.booking import Booking


class BookingServices:
    @staticmethod
    def create_booking(room_id: int, date_start: date, date_end: date):
        if not BookingRepository.is_available(room_id, date_start, date_end):
            raise ValidationError("Комната забронирована на эти даты")
        return BookingRepository.create_booking(room_id, date_start, date_end)

    @staticmethod
    def delete_booking(booking_id: int) -> None:
        try:
            booking = BookingRepository.get_booking_by_id(booking_id)
            if not booking:
                raise ObjectDoesNotExist(f"Бронирование с ID {booking_id} не найдено")
            BookingRepository.delete_booking(booking_id)
        except ObjectDoesNotExist as e:
            raise ValidationError(str(e))
        except Exception as e:
            raise ValidationError(f"Ошибка при удалении бронирования: {str(e)}")

    @staticmethod
    def get_bookings_for_room(room_id: int) -> list[Booking]:
        return BookingRepository.get_bookings_by_room(room_id)
