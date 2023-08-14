from django.shortcuts import render, redirect
from .models import Event, AppUser
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm
# Create your views here.


def index(request):
    events = Event.objects.get_queryset()
    context = {"events": events}
    return render(request, "index.html", context)


def login_user(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')
                return redirect('index')

        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('/')

def artist_listing(request):
    artists = AppUser.objects.filter(is_artist=True)
    return render(request, 'artist_listing.html', {'artists': artists})

def organizer_listing(request):
    organizers = AppUser.objects.filter(is_organizer=True)
    return render(request, 'organizer_listing.html', {'organizers': organizers})
