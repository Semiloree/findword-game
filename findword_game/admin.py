from django.contrib import admin

# Register your models here.
# findword_game/admin.py
from .models import Word
from django.contrib import admin
from .models import Word, Feedback, Score, Achievement

@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('word', 'definition')
    search_fields = ('text',)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at', 'message')
    list_filter = ('submitted_at',)
    search_fields = ('user__username', 'message')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display  = ("user", "score", "date_played")
    list_filter   = ("date_played",)
    search_fields = ("user__username",)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display  = ('user', 'achievement', 'details', 'date_earned')
    list_filter   = ('achievement', 'date_earned')
    search_fields = ('user__username', 'details')
