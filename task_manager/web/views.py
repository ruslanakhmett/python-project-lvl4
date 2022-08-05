from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import login, logout
from .forms import UserLoginForm, SignUpForm
from django.contrib.auth import authenticate
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User



class IndexView(View):
    def get(self, request):
        return render(request, 'pages/index.html')


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Вы разлогинены')
        return redirect('index')


class LoginPageView(View):
    template_name = 'pages/login.html'

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Вы залогинены')
                return redirect('index')
            else:
                messages.add_message(request, messages.ERROR, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
        return render(request, self.template_name, context={'form': form})
        

class SignUpView(CreateView):
    template_name = 'pages/signup.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, context={'form': form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Пользователь успешно зарегистрирован')
            return redirect('login')
        return render(request, self.template_name, {'form': form})
    

class UsersShowView(View):
    template_name = 'pages/users.html'
    
    def get(self, request):
        return render(request, self.template_name, context={'users': User.objects.all()})
