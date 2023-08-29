import datetime

from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, AppUser, Ticket, Application, Post
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
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
        return render(request, 'login.html', {'form': form, 'msg': 'Invalid username or password'})


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
    return render(request, 'register.html', {'form': form})


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
        number_of_tickets = int(request.POST.get('number_of_tickets', 1))
        event.available_tickets -= number_of_tickets
        event.save()

        app_user = get_object_or_404(AppUser, pk=request.user.pk)
        for i in range(0, number_of_tickets):
            ticket = Ticket(event=event, user_profile=app_user)
            ticket.save()

        return redirect('purchase_confirm')

    return render(request, 'buy_ticket.html', {'event': event})


def tickets(request):
    tickets = Ticket.objects.filter(user_profile=request.user)
    return render(request, 'tickets.html', {'tickets': tickets})


def create_event(request):
    if request.method == 'GET':
        artists = AppUser.objects.filter(is_artist=True)
        print(artists)
        return render(request, 'create_event.html', {"artists": artists})
    elif request.method == "POST":
        title = request.POST['title']
        loc = request.POST['location']
        img = request.FILES['image']
        date = request.POST['date']
        desc = request.POST['description']
        ticketnum = request.POST['ticketsNum']
        ticketsPrice = request.POST['ticketsPrice']
        artists = AppUser.objects.filter(id__in=request.POST.getlist('artists[]'))
        organizer = request.user
        event = Event.objects.create(title=title, location=loc, image=img, date=date, description=desc,
                                     ticketsPrice=ticketsPrice, available_tickets=ticketnum, organizer=organizer)
        event.artists.set(artists)
        event.save()
        return redirect('index')


def event_apply(request, event_id):
    event = Event.objects.get(id=event_id)

    if request.method == 'GET':
        return render(request, 'event_apply.html', {"event": event})

    elif request.method == "POST":
        motiv = request.POST['motivation']
        num = request.POST['phone_num']
        cv = request.FILES['cv']
        occ = request.POST['occupation']
        artist = request.user
        application = Application.objects.create(motivation=motiv, phone_number=num, cv=cv, occupation=occ, event=event,
                                                 artist=artist)
        application.save()
        return redirect('index')


def my_events(request):
    events = Event.objects.filter(organizer=request.user)
    return render(request, 'my_events.html', {"events": events})


def event_applications(request, event_id):
    event = Event.objects.get(id=event_id)
    apps = Application.objects.filter(event=event)
    if request.method == 'GET':
        return render(request, 'event_applications.html', {"applications": apps, "event": event})


def profile(request, user_id):
    user = get_object_or_404(AppUser, pk=user_id)
    if user.is_artist:
        event_num = Event.objects.filter(artists__id=user_id).count()
    elif user.is_organizer:
        event_num = Event.objects.filter(organizer_id=user_id).count()
    else:
        event_num = Ticket.objects.filter(user_profile_id=user_id).distinct().count()
    posts = Post.objects.filter(author_id=user_id).order_by('-date')
    return render(request, 'profile.html', {'user': user, 'event_num': event_num, 'posts': posts})


def event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    tickets = Ticket.objects.filter(event=event)
    return render(request, 'event_details.html', {'event': event, 'tickets': tickets})


def help(request):
    return render(request, "help.html")


def accept_application(request, application_id):
    application = Application.objects.get(id=application_id)
    application.status = "Accepted"
    application.save()
    event = Event.objects.get(id=application.event.pk)
    event.artists.add(request.user)
    event.save()
    apps = Application.objects.filter(event=event, status="Waiting")
    return render(request, 'event_applications.html',
                  {"applications": apps, "feedback": "Successfully accepted the application!"})


def deny_application(request, application_id):
    application = Application.objects.get(id=application_id)
    application.status = "Denied"
    application.save()
    apps = Application.objects.filter(event=application.event, status="Waiting")
    return render(request, 'event_applications.html',
                  {"applications": apps, "feedback": "Successfully denied the application!"})


def my_applications(request):
    applications = Application.objects.filter(artist=request.user)
    return render(request, 'my_applications.html', {"applications": applications})


def add_post(request):
    descr = request.POST['descr']
    author = request.user
    date = datetime.datetime.now()
    if 'file' in request.FILES and request.FILES['file']:
        file = request.FILES['file']
        post = Post.objects.create(file=file, date=date, description=descr, author=author)
    else:
        post = Post.objects.create(date=date, description=descr, author=author)
    post.save()
    return redirect('profile', user_id=request.user.id)


def delete_post(request, post_id):
    Post.objects.filter(id=post_id).delete()
    return redirect('profile', user_id=request.user.id)
