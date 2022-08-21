from curses import color_content
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Statuses, Tasks, Labels



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


class StatusCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    name = forms.CharField(error_messages={'unique': 'Task status с таким Имя уже существует.'},
                           label=_("Имя"),
                           widget=forms.TextInput(attrs={"class": "form-control",
                                                         'placeholder': _('Имя')}))
    class Meta:
        model = Statuses
        fields = ("name",)


class LabelCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    name = forms.CharField(error_messages={'unique': 'Label с таким Имя уже существует.'},
                           label=_("Имя"),
                           widget=forms.TextInput(attrs={"class": "form-control",
                                                         'placeholder': _('Имя')}))
    class Meta:
        model = Labels
        fields = ("name",)


class TaskCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    name = forms.CharField(error_messages={'unique': 'Task с таким Имя уже существует.'},
                           label=_("Имя"), 
                           widget=forms.TextInput(attrs={"class": "form-control", 
                                                         'placeholder': _('Имя')}))
    description = forms.CharField(label=_("Описание"),
                                  widget=forms.Textarea(attrs={"class": "form-control", 
                                                               'rows': 4, 
                                                               'placeholder': _('Описание')}))
    status = forms.ModelChoiceField(
        label=_("Статус"),
        queryset=Statuses.objects.all(),
        required=True,  
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tasks
        fields = ("name",
                  "description",
                  "status")