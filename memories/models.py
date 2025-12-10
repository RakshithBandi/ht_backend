from django.db import models

class Memory(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file = models.TextField()  # Storing base64 string for images/videos
    type = models.CharField(max_length=10, choices=[('image', 'Image'), ('video', 'Video')])
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Memories"
        ordering = ['-createdAt']
