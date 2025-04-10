from django.db import models


class Booking(models.Model):
    room = models.ForeignKey(
        "rooms.Room", on_delete=models.CASCADE, related_name="bookings"
    )
    date_start = models.DateField()
    date_end = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bookings"
