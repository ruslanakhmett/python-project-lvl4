from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label=_("Имя пользователя"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label=_("Пароль"), widget=forms.PasswordInput(attrs={"class": "form-control"})  # noqa 501
    )


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_("Имя"), widget=forms.TextInput())
    last_name = forms.CharField(label=_("Фамилия"), widget=forms.TextInput())

    class Meta:
        model = User
        fields = ("first_name",
                  "last_name",
                  "username",
                  "password1",
                  "password2")


class StatusCreateForm(forms.Form):
    name = forms.CharField(label=_("Имя"), widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': _('Имя')}))


class LabelCreateForm(forms.Form):
    name = forms.CharField(label=_("Имя"), widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': _('Имя')}))
