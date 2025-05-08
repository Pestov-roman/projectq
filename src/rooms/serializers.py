from rest_framework import serializers
from src.core.models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price_per_night", "created_at"]


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["description", "price_per_night"]
