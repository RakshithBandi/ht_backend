from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Question(models.Model):
    question_text = models.TextField(blank=True, null=True)
    question_image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    year = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.question_text and not self.question_image:
            raise ValidationError('Question must have either text or an image.')

    def __str__(self):
        return f"Q: {self.question_text[:50] if self.question_text else 'Image Question'} ({self.year})"

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'question')  # Prevent duplicate answers

class UserScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='quiz_score')
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}: {self.total_points}"

class QuizSettings(models.Model):
    is_leaderboard_visible = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Quiz Settings"

    def __str__(self):
        return "Quiz Configuration"
