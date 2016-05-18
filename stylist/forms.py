from django.contrib.auth.forms import UserCreationForm
from django import forms

from stylist.models import MyUser


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = MyUser
        widgets = {'woeid': forms.HiddenInput()}
        fields = ("username", "city", "zip_code", "woeid")
