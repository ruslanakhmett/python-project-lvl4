from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class UserLoginForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
    
    username = forms.CharField(
        label=_("Имя пользователя"),
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label=_("Пароль"), widget=forms.PasswordInput(attrs={"class": "form-control"})  # noqa 501
    )


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    name = forms.CharField(label=_("Имя"), widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': _('Имя')}))


class LabelCreateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    name = forms.CharField(label=_("Имя"), widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': _('Имя')}))
