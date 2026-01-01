from django.db import models
from django.conf import settings

class GPUSlot(models.Model):
    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    # Add more fields like GPU type, specs, etc. later

    def __str__(self):
        return f'{self.name} ({ "Available" if self.is_available else "Booked"})'

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    gpu_slot = models.ForeignKey(GPUSlot, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.gpu_slot.name} - {self.start_time.strftime("%Y-%m-%d %H:%M")}'
