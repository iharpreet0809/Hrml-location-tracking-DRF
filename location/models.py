from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    """
    Model to store employee location tracking data.
    """
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='locations',
        help_text='Employee who recorded this location'
    )
    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        help_text='Latitude coordinate (-90 to 90)'
    )
    longitude = models.DecimalField(
        max_digits=11,
        decimal_places=7,
        help_text='Longitude coordinate (-180 to 180)'
    )
    accuracy = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        help_text='GPS accuracy in meters'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text='When the location was recorded'
    )

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['employee', '-timestamp']),
            models.Index(fields=['timestamp']),
        ]
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f"{self.employee.username} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
