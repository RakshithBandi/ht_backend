from django.db import models

class Game(models.Model):
    gameName = models.CharField(max_length=200)
    participantsCount = models.IntegerField(default=0)
    description = models.TextField()
    winnerName = models.CharField(max_length=200)
    winnerImage = models.TextField(blank=True, null=True)  # Storing base64 string
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gameName
