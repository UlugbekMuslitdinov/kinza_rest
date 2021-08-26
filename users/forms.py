from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

YEAR_CHOICES = [str(i) for i in range(1930, 2020)]


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name')
        labels = {'username': ('Ваше имя')}


class MyAuthForm(forms.Form):
    username = forms.CharField(max_length=100, label='Phone number')
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    password = forms.CharField(max_length=10)