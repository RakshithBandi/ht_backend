from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Announcement

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
