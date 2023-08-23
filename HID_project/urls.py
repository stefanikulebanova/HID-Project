"""
URL configuration for HID_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
import project_app.views as views

urlpatterns = [
                  path('index/', RedirectView.as_view(url='index/', permanent=False)),
                  path('', views.index, name="index"),
                  path('login/', views.login_user, name="login"),
                  path('logout/', views.logout_user, name="logout"),
                  path('register/', views.register_user, name="register"),
                  path('organizers/', views.organizer_listing, name="organizer_listing"),
                  path('create_event/', views.create_event, name="create_event"),
                  path('event_apply/<int:event_id>/', views.event_apply, name="event_apply"),
                  path('event_applications/<int:event_id>/', views.event_applications, name="event_applications"),
                  path('accept_application/<int:application_id>/', views.accept_application, name="accept_application"),
                  path('deny_application/<int:application_id>/', views.deny_application, name="deny_application"),
                  path('my_applications', views.my_applications, name="my_applications"),
                  path('my_events/', views.my_events, name="my_events"),
                  path('artists/', views.artist_listing, name="artist_listing"),
                  path('purchase_confirm/', views.purchase_confirm, name="purchase_confirm"),
                  path('application_confirm/', views.application_confirm, name="application_confirm"),
                  path('buy_ticket/<int:event_id>/', views.buy_ticket, name='buy_ticket'),
                  path('tickets/', views.tickets, name='tickets'),
                  path('help/', views.help, name='help'),
                  path('profile/<int:user_id>/', views.profile, name='profile'),
                  path('add_post', views.add_post, name='add_post'),
                  path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
                  path('event_details/<int:event_id>', views.event_details, name='event_details'),
                  path('admin/', admin.site.urls),                  
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
