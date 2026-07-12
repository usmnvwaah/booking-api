from django.db import models
from django.contrib.auth.models import User


class Resource(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ]

    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    start = models.DateTimeField()
    end = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start']
# Create your models here.
