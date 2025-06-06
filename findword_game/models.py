from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# findword_game/models.py

class Word(models.Model):
    word = models.CharField(max_length=100, unique=True)
    definition = models.TextField()

    def __str__(self):
        return self.word


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}"
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user or 'Anonymous'}"
    
class Achievement(models.Model):
    ACHIEVEMENT_CHOICES = [
        ('level_complete', 'Completed a Level'),
        ('quick_streak',    'Quick Find Streak'),
    ]
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement   = models.CharField(max_length=20, choices=ACHIEVEMENT_CHOICES)
    date_earned   = models.DateTimeField(auto_now_add=True)
    details       = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username} – {self.get_achievement_display()}"
