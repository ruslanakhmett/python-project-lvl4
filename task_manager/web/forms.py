from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Statuses, Tasks


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})  # noqa 501
    )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput())
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput())

    class Meta:
        model = User
        fields = ("first_name",
                  "last_name",
                  "username",
                  "password1",
                  "password2")


class StatusCreateForm(forms.Form):
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Имя'}))
    
class LabelCreateForm(forms.Form):
    name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Имя'}))


# class TasksCreateForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     description = forms.CharField(max_length=1000)
#     status = forms.ModelMultipleChoiceField(queryset=Statuses.objects.all())