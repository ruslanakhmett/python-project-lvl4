from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Statuses, Tasks, Labels, MyUser


class UserLoginForm(forms.Form):

    username = forms.CharField(
        label_suffix="",
        label=_("Имя пользователя"),
        widget=forms.TextInput(attrs={"class": "form-control", "autofocus": True}),
    )
    password = forms.CharField(
        label_suffix="",
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={"class": "form-control"}),  # noqa 501
    )


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "password1", "password2")


class StatusCreateForm(forms.ModelForm):

    name = forms.CharField(
        label_suffix="",
        error_messages={"unique": "Task status с таким Имя уже существует."},
        label=_("Имя"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Имя"), "autofocus": True}
        ),
    )

    class Meta:
        model = Statuses
        fields = ("name",)


class LabelCreateForm(forms.ModelForm):

    name = forms.CharField(
        label_suffix="",
        error_messages={"unique": "Label с таким Имя уже существует."},
        label=_("Имя"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Имя"), "autofocus": True}
        ),
    )

    class Meta:
        model = Labels
        fields = ("name",)


class TaskCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    name = forms.CharField(
        error_messages={"unique": "Task с таким Имя уже существует."},
        label=_("Имя"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Имя"), "autofocus": True}
        ),
    )
    description = forms.CharField(
        label=_("Описание"),
        required=False,
        widget=forms.Textarea(
            attrs={"class": "form-control", "rows": 4, "placeholder": _("Описание")}
        ),
    )
    status = forms.ModelChoiceField(
        label=_("Статус"),
        queryset=Statuses.objects.all(),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    executor = forms.ModelChoiceField(
        label=_("Исполнитель"),
        queryset=MyUser.objects.all().exclude(username="admin"),
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    labels = forms.ModelMultipleChoiceField(
        label=_("Метки"),
        queryset=Labels.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Tasks
        fields = ("name", "description", "status", "executor", 'labels')
