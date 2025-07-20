from django.db import models
from django.conf import settings
# Create your models here.
class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    message = models.TextField()
    file = models.FileField(upload_to='notifications/', null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    