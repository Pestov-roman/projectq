from django.db import models


class Room(models.Model):
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_room = models.DecimalField(max_digits=5, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rooms"
