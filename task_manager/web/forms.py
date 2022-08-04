from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


# class UserRegisterForm(UserCreationForm):
#     last_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={"class": "form-control", 'autocomplete': "off"}))
#     first_name =forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={"class": "form-control", 'autocomplete': "off"}))
#     user_name = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control", 'autocomplete': "off"}))
#     password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))
#     password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={"class": "form-control"}))


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={"class": "form-control", 'autocomplete': "off"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-control"}))

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'username', 
            'password1', 
            'password2', 
            ]