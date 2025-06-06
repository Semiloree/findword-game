from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('game/', views.game_view, name='game'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('save-score/', views.save_score, name='save_score'),  # If using JS
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('award-achievement/', views.award_achievement, name='award_achievement'),
]
