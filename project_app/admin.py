from django.contrib import admin
from .models import AppUser, Event, Ticket

# Register your models here.


class AppUserAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass


class TicketAdmin(admin.ModelAdmin):
    pass


admin.site.register(AppUser, AppUserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Ticket, TicketAdmin)
