from django.db import models
from django.core.exceptions import ValidationError
from src.rooms.models import Room


class Booking(models.Model):
    room: Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in: models.DateField = models.DateField()
    check_out: models.DateField = models.DateField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    def clean(self) -> None:
        if self.check_in and self.check_out and self.check_in >= self.check_out:
            raise ValidationError("Check-in date must be before check-out date")

    def __str__(self) -> str:
        return f"Booking for Room {self.room.number} from {self.check_in} to {self.check_out}"
