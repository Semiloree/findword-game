from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random
import string
from .models import Score , Achievement
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Feedback
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'home.html')

def register_view(request):

    if request.user.is_authenticated:
        return redirect('game')
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validate form
        if password != confirm_password:
            messages.error(request, 'Passwords do not match', extra_tags='confirm')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email has already been registered', extra_tags='email')
        else:
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Account already exists', extra_tags='email')
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name)
                user.save()
                messages.success(request, 'Account created successfully!')
                return redirect('login')

    return render(request, 'register.html')


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):

    if request.user.is_authenticated:
        return redirect('game')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email', extra_tags='email')
            return render(request, 'login.html')

        user = authenticate(request, username=user_obj.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect password', extra_tags='password')
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def generate_grid(size=10):
    return [[random.choice(string.ascii_uppercase) for _ in range(size)] for _ in range(size)]

def game_view(request):
    grid_size = 10  # You can adjust based on difficulty level
    grid = generate_grid(grid_size)
    return render(request, 'findword_game/game.html', {'grid': grid})


@login_required
def save_score(request):
    if request.method == 'POST':
        score_value = int(request.POST.get('score', 0))
        Score.objects.create(user=request.user, score=score_value)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
    

def leaderboard(request):
    top_scores = Score.objects.order_by('-score')[:10]
    return render(request, 'leaderboard.html', {'top_scores': top_scores})


# findword_game/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Feedback

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        # Grab “message” from POST body:
        msg = request.POST.get('message', '').strip()
        if not msg:
            return JsonResponse({'status': 'error', 'reason': 'empty_message'}, status=400)

        # If the user is authenticated, attach it; otherwise leave as None
        user = request.user if request.user.is_authenticated else None

        # Create the Feedback row
        Feedback.objects.create(user=user, message=msg)
        return JsonResponse({'status': 'success'})

    # If not a POST, return a simple error
    return JsonResponse({'status': 'error', 'reason': 'invalid_method'}, status=400)

@csrf_exempt
def award_achievement(request):
    if request.method == 'POST' and request.user.is_authenticated:
        code = request.POST.get('achievement')
        details = request.POST.get('details', '')
        if code in dict(Achievement.ACHIEVEMENT_CHOICES).keys():
            Achievement.objects.create(user=request.user, achievement=code, details=details)
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'reason': 'invalid_code'}, status=400)
    return JsonResponse({'status': 'error', 'reason': 'not_authenticated_or_method'}, status=403)
