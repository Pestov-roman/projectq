from django.test import TestCase
from datetime import date
from src.core.models import Room
from src.bookings.models import Booking
from src.core.repositories.room_repository import RoomRepository
from src.core.repositories.booking_repository import BookingRepository


class RoomRepositoryTest(TestCase):
    def test_create_room_ok(self):
        room = RoomRepository.create_room(description="Luxe", price=1000)
        self.assertEqual(room.description, "Luxe")
        self.assertEqual(room.price, 1000)

    def test_delete_room_ok(self):
        room = RoomRepository.create_room(description="Room to delete", price=100)
        self.assertEqual(room.description, "Room to delete")
        self.assertEqual(room.price, 100)

    def test_delete_room_nonexistent(self):
        initial_count = Room.objects.count()
        RoomRepository.delete_room(room_id=999999)
        self.assertEqual(Room.objects.count(), initial_count)

    def test_get_rooms_default_order(self):
        r1 = RoomRepository.create_room(description="Room 1", price=500)
        r2 = RoomRepository.create_room(description="Room 2", price=1000)
        rooms = RoomRepository.get_rooms()
        self.assertListEqual([r.id for r in rooms], [r1.id, r2.id])

    def test_get_rooms_price_asc(self):
        r1 = RoomRepository.create_room(description="Room 1", price=500)
        r2 = RoomRepository.create_room(description="Room 2", price=1000)
        rooms = RoomRepository.get_rooms(order_by="price", ascending=True)
        self.assertListEqual([r.id for r in rooms], [r1.id, r2.id])

    def test_get_rooms_price_desc(self):
        r1 = RoomRepository.create_room(description="Room 1", price=500)
        r2 = RoomRepository.create_room(description="Room 2", price=1000)
        rooms = RoomRepository.get_rooms(order_by="price", ascending=False)
        self.assertListEqual([r.id for r in rooms], [r2.id, r1.id])


class BookingRepositoryTest(TestCase):
    def setUp(self):
        self.room = RoomRepository.create_room(description="Test room", price=400)

    def test_create_booking_ok(self):
        booking = BookingRepository.create_booking(
            room_id=self.room.id,
            date_start=date(2024, 1, 10),
            date_end=date(2024, 1, 15),
        )
        self.assertEqual(booking.room_id, self.room.id)
        self.assertEqual(booking.date_start, date(2024, 1, 10))
        self.assertEqual(booking.date_end, date(2024, 1, 15))

    def test_delete_booking_ok(self):
        booking = BookingRepository.create_booking(
            room_id=self.room.id,
            date_start=date(2024, 3, 10),
            date_end=date(2024, 3, 15),
        )
        booking_id = booking.id
        BookingRepository.delete_booking(booking_id)
        self.assertFalse(Booking.objects.filter(id=booking_id).exists())

    def test_get_bookings_for_room_ordered_by_date_start(self):
        b1 = BookingRepository.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 3, 10),
            date_end=date(2023, 3, 12),
        )
        b2 = BookingRepository.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 3, 1),
            date_end=date(2023, 3, 5),
        )
        bookings = BookingRepository.get_bookings_by_room(self.room.id)
        self.assertListEqual([b.id for b in bookings], [b2.id, b1.id])

    def test_bookings_overlap_true(self):
        BookingRepository.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 4, 1),
            date_end=date(2023, 4, 5),
        )
        overlap = not BookingRepository.is_available(
            room_id=self.room.id, date_start=date(2023, 4, 3), date_end=date(2023, 4, 7)
        )
        self.assertTrue(overlap)

    def test_bookings_overlap_false(self):
        BookingRepository.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 5, 1),
            date_end=date(2023, 5, 5),
        )
        overlap = not BookingRepository.is_available(
            room_id=self.room.id,
            date_start=date(2023, 5, 6),
            date_end=date(2023, 5, 10),
        )
        self.assertFalse(overlap)

    def test_bookings_overlap_edge_case(self):
        BookingRepository.create_booking(
            room_id=self.room.id,
            date_start=date(2023, 6, 1),
            date_end=date(2023, 6, 10),
        )
        overlap = not BookingRepository.is_available(
            room_id=self.room.id,
            date_start=date(2023, 6, 10),  # Начинается в тот же день
            date_end=date(2023, 6, 15),
        )
        self.assertFalse(overlap)
