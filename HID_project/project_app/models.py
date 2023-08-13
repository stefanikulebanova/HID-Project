from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AppUser(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    bio = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_organizer = models.BooleanField(default=False)
    is_artist = models.BooleanField(default=False)


class Event(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="events", default="./templates/img.png")
    date = models.DateTimeField()
    available_tickets = models.IntegerField()
    artists = models.ManyToManyField(AppUser, related_name="artists")
    organizer = models.ForeignKey(AppUser, related_name="organizer", on_delete=models.CASCADE)


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField
    qr_code = models.ImageField(upload_to="ticket_qr")





