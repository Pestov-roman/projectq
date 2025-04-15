from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date

from src.rooms.models import Room
from src.bookings.models import Booking
from src.core.services.room_services import RoomServices
from src.core.services.booking_services import BookingServices


class RoomServicesTest(TestCase):
    def test_create_room_ok(self):
        room = RoomServices.create_room(description="Test Room", price=1500)
        self.assertIsNotNone(room.id)
        self.assertEqual(room.description, "Test Room")
        self.assertEqual(room.price, 1500)

    def test_delete_room_ok(self):
        room = RoomServices.create_room(description="Room to delete", price=500)
        room_id = room.id
        RoomServices.delete_room(room_id)
        self.assertFalse(Room.objects.filter(id=room_id).exists())

    def test_list_rooms_default(self):
        r1 = RoomServices.create_room(description="Room 1", price=1000)
        r2 = RoomServices.create_room(description="Room 2", price=500)
        rooms = RoomServices.list_rooms()
        self.assertEqual([r.id for r in rooms], [r1.id, r2.id])

    def test_list_rooms_by_price_desc(self):
        r1 = RoomServices.create_room(description="Room 1", price=500)
        r2 = RoomServices.create_room(description="Room 2", price=1000)
        rooms = RoomServices.list_rooms(order_by="price", ascending=False)
        self.assertEqual([r.id for r in rooms], [r2.id, r1.id])


class BookingServicesTest(TestCase):
    def setUp(self):
        self.room = RoomServices.create_room(description="Test Room", price=999)

    def test_create_booking_ok(self):
        booking = BookingServices.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 7, 1),
            date_end=date(2023, 7, 5),
        )
        self.assertIsNotNone(booking.id)
        self.assertEqual(booking.room_id, self.room.id)
        self.assertEqual(booking.date_start, date(2023, 7, 1))
        self.assertEqual(booking.date_end, date(2023, 7, 5))

    def test_create_booking_overlap_fail(self):
        BookingServices.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 8, 1),
            date_end=date(2023, 8, 5),
        )
        with self.assertRaises(ValidationError) as ctx:
            BookingServices.create_booking(
                room_id=self.room.id,
                date_start=date(2023, 8, 4),
                date_end=date(2023, 8, 10),
            )
        self.assertIn("Комната забронирована на эти даты", str(ctx.exception))

    def test_delete_booking_ok(self):
        booking = BookingServices.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 9, 1),
            date_end=date(2023, 9, 5),
        )
        booking_id = booking.id
        BookingServices.delete_booking(booking_id)
        self.assertFalse(Booking.objects.filter(id=booking_id).exists())

    def test_list_bookings_for_room(self):
        b1 = BookingServices.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 10, 5),
            date_end=date(2023, 10, 10),
        )
        b2 = BookingServices.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 10, 1),
            date_end=date(2023, 10, 3),
        )
        bookings = BookingServices.get_bookings_for_room(self.room.id)
        self.assertEqual([b.id for b in bookings], [b2.id, b1.id])
