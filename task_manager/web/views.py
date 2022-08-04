from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import login, logout
from .forms import UserLoginForm, SignUpForm
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView


class IndexView(View):
    def get(self, request):
        return render(request, 'pages/index.html')


class LoginPageView(View):
    template_name = 'pages/login.html'
    form = UserLoginForm()

    def get(self, request):
        return render(request, self.template_name, context={'form': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = 'Вы залогинены'
            else:
                message = 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        return render(
        request, self.template_name, context={'form': form, 'message': message})
        

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'pages/signup.html'