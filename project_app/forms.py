from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AppUser


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = AppUser
        fields = ('username', 'email', 'password1', 'password2', 'is_organizer', 'is_artist', 'bio', 'phone_number', 'image' )

    def save(self, commit = True) -> Any:
        user = super().save(commit=False)
        user.is_artist = self.cleaned_data.get('is_artist')
        user.is_organizer = self.cleaned_data.get('is_organizer')
        user.bio = self.cleaned_data.get('bio')
        user.phone_number = self.cleaned_data.get('phone_number')
        image = self.cleaned_data.get('image')
        if image:
            user.image = image

        if commit:
            user.save()
        return user
