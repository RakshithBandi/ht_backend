from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_picture = models.TextField(null=True, blank=True)  # Base64 encoded image
    
    def __str__(self):
        return f"{self.user.username}'s profile"
