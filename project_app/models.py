import os
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class AppUser(AbstractUser):
    phone_number = models.CharField(max_length=255)
    bio = models.CharField(max_length=400)
    is_organizer = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)
    image = models.ImageField(upload_to="users", default="users/person.png")


class Event(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="events", default="events/event1.jpg")
    date = models.DateTimeField()
    description = models.CharField(max_length=300, default="Description for event. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor... ")
    available_tickets = models.IntegerField()
    ticket_price = models.IntegerField(default=10)
    artists = models.ManyToManyField(AppUser, related_name="artists")
    organizer = models.ForeignKey(AppUser, related_name="organizer", on_delete=models.CASCADE)


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to="ticket_qr", default="ticket_qr/qrcode.png")
    price = models.IntegerField(default=10)


class Application(models.Model):
    motivation = models.CharField(max_length=400)
    cv = models.FileField(upload_to="cover_letters")
    occupation = models.CharField(max_length=255)
    apply_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=255)
    status = models.CharField(max_length=150, default="Waiting")
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    artist = models.ForeignKey(AppUser, on_delete=models.CASCADE)


class Post(models.Model):
    file = models.FileField(upload_to="posts", blank = True)
    description = models.TextField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension






