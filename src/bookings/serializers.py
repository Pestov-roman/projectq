from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "room", "check_in", "check_out", "created_at"]


class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["room", "check_in", "check_out"]
