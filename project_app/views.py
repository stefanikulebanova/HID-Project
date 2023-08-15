import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, AppUser, Ticket
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, RegisterForm


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

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form':form})


def artist_listing(request):
    artists = AppUser.objects.filter(is_artist=True)
    return render(request, 'artist_listing.html', {'artists': artists})


def organizer_listing(request):
    organizers = AppUser.objects.filter(is_organizer=True)
    return render(request, 'organizer_listing.html', {'organizers': organizers})


def purchase_confirm(request):
    return render(request, 'purchase_confirmation.html')


def application_confirm(request):
    return render(request, 'application_confirmation.html')


def buy_ticket(request, event_id):
    # item = get_object_or_404(Item, pk=item_id)
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        number_of_tickets = request.POST.get('number_of_tickets')
        event.available_tickets -= int(number_of_tickets)
        event.save()

        print(event)
        print(AppUser)
        print(datetime.date.today())

        print(request.user.pk)

        app_user = get_object_or_404(AppUser, pk=request.user.pk)

        ticket = Ticket(event=event, user_profile=app_user)
        ticket.save()

        return redirect('purchase_confirm')

    return render(request, 'buy_ticket.html', {'event': event})


def tickets(request):
    user = get_object_or_404(AppUser, pk=request.user.pk)
    tickets_by_user = Ticket.objects.filter(user_profile=user)

    return render(request, 'tickets.html', {'tickets': tickets_by_user})
