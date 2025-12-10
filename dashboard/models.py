from django.db import models

class Announcement(models.Model):
    heading = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.heading} ({self.year})"

    class Meta:
        ordering = ['-created_at']
