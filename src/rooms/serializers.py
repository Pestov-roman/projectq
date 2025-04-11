from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "description", "price", "created_at"]


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["description", "price"]
