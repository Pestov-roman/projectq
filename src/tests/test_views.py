from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date

from src.core.models import Room
from src.bookings.models import Booking


class RoomAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = reverse("room-create")
        self.delete_url = reverse("room-delete")
        self.list_url = reverse("room-list")

    def test_create_room_success(self):
        data = {"description": "Sea view", "price_per_night": "1500", "capacity": 2}
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("room_id", response.data)
        room_id = response.data["room_id"]
        self.assertTrue(Room.objects.filter(id=room_id).exists())

    def test_create_room_invalid_data(self):
        data = {"description": "No price"}
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_room_success(self):
        room = Room.objects.create(
            description="Test Room", price_per_night=123, capacity=2
        )
        url = f"{self.delete_url}?room_id={room.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Room.objects.filter(id=room.id).exists())

    def test_delete_room_no_param(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_list_rooms_default(self):
        r1 = Room.objects.create(description="R1", price_per_night=100, capacity=2)
        r2 = Room.objects.create(description="R2", price_per_night=200, capacity=3)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["id"], r1.id)
        self.assertEqual(response.data[1]["id"], r2.id)

    def test_list_rooms_price_desc(self):
        r1 = Room.objects.create(description="R1", price_per_night=100, capacity=2)
        r2 = Room.objects.create(description="R2", price_per_night=200, capacity=3)
        url = f"{self.list_url}?order_by=price_per_night&asc=0"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([res["id"] for res in response.data], [r2.id, r1.id])


class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = reverse("booking-create")
        self.delete_url = reverse("booking-delete")
        self.list_url = reverse("booking-list")

        self.room = Room.objects.create(
            description="Test Room", price_per_night=999, capacity=2
        )

    def test_create_booking_success(self):
        data = {
            "room": self.room.id,
            "date_start": "2023-07-01",
            "date_end": "2023-07-05",
        }
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("booking_id", response.data)

        booking_id = response.data["booking_id"]
        self.assertTrue(Booking.objects.filter(id=booking_id).exists())

    def test_create_booking_overlap(self):
        Booking.objects.create(
            room=self.room, date_start=date(2023, 8, 1), date_end=date(2023, 8, 5)
        )

        data = {
            "room": self.room.id,
            "date_start": "2023-08-03",
            "date_end": "2023-08-07",
        }
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("Комната забронирована на эти даты", response.data["error"])

    def test_create_booking_invalid_dates(self):
        data = {
            "room": self.room.id,
            "date_start": "not-a-date",
            "date_end": "2023-09-10",
        }
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date_start", response.data)

    def test_delete_booking_success(self):
        booking = Booking.objects.create(
            room=self.room, date_start=date(2023, 9, 1), date_end=date(2023, 9, 5)
        )
        url = f"{self.delete_url}?booking_id={booking.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Booking.objects.filter(id=booking.id).exists())

    def test_delete_booking_no_id(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_list_bookings_ok(self):
        b1 = Booking.objects.create(
            room=self.room, date_start=date(2023, 10, 5), date_end=date(2023, 10, 7)
        )
        b2 = Booking.objects.create(
            room=self.room, date_start=date(2023, 10, 1), date_end=date(2023, 10, 3)
        )
        url = f"{self.list_url}?room_id={self.room.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        bookings_data = response.json()
        self.assertEqual(len(bookings_data), 2)
        self.assertEqual(bookings_data[0]["booking_id"], b2.id)
        self.assertEqual(bookings_data[1]["booking_id"], b1.id)

    def test_list_bookings_no_room_id(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
