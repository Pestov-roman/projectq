from django.db import models


class Room(models.Model):
    number: str = models.CharField(max_length=10, unique=True)
    capacity: int = models.PositiveIntegerField()
    price_per_night: float = models.DecimalField(max_digits=10, decimal_places=2)
    description: str = models.TextField()
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["number"]

    def __str__(self) -> str:
        return f"Room {self.number}"
