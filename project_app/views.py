from django.shortcuts import render
from .models import Event

# Create your views here.


def index(request):
    events = Event.objects.get_queryset()
    context = {"events": events}
    return render(request, "index.html", context)

