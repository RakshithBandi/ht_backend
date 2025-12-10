from django.db import models

class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.TextField(blank=True, null=True)  # Storing base64 string
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
