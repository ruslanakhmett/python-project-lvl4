from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView

from .forms import SignUpForm, UserLoginForm, StatusCreateForm
from .models import Statuses


class IndexView(View):
    def get(self, request):
        return render(request, "pages/index.html")


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, "Вы разлогинены")
        return redirect("index")


class LoginPageView(View):
    template_name = "pages/login.html"

    def get(self, request):
        form = UserLoginForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.add_message(request,
                                     messages.SUCCESS,
                                     "Вы залогинены")
                return redirect("index")
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Пожалуйста, введите правильные имя пользователя и пароль. \
                                         Оба поля могут быть \
                                             чувствительны к регистру.",
                )
        return render(request, self.template_name, context={"form": form})


class SignUpView(CreateView):
    template_name = "pages/signup.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, context={"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Пользователь успешно зарегистрирован"
            )
            return redirect("login")
        return render(request, self.template_name, {"form": form})


class UsersShowView(View):
    template_name = "pages/users.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            context={"users": User.objects.all().exclude(username="admin")},
        )


class UpdateUserView(View):
    template_name = "pages/user_update.html"

    def get(self, request, **kwargs):

        if request.user.is_authenticated:
            form = SignUpForm(instance=request.user)

            user_id_from_link = kwargs["pk"]
            if request.user.pk == user_id_from_link:
                return render(request,
                              self.template_name,
                              context={"form": form})
            messages.add_message(
                request,
                messages.ERROR,
                "У вас нет прав для изменения другого пользователя.",
                fail_silently=True,
            )
            return redirect("users")
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Вы не авторизованы! Пожалуйста, выполните вход.",
                fail_silently=True,
            )
            return redirect("login")

    def post(self, request):
        form = SignUpForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Пользователь успешно изменен"
            )
            return redirect("users")
        return render(request, self.template_name, context={"form": form})


class DeleteUserView(View):
    template_name = "pages/user_delete.html"

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            user_id_from_link = kwargs["pk"]
            if request.user.id == user_id_from_link:
                return render(request, self.template_name)
            messages.add_message(
                request,
                messages.ERROR,
                "У вас нет прав для изменения другого пользователя.",
                fail_silently=True,
            )
            return redirect("users")
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Вы не авторизованы! Пожалуйста, выполните вход.",
                fail_silently=True,
            )
            return redirect("login")

    def post(self, request, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
            user.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Пользователь успешно удален",
                fail_silently=True,
            )
        except Exception as error: 
            messages.add_message(
                request,
                messages.ERROR,
                error.message,
                fail_silently=True,
            )
        return redirect('users')


class StatusesShowView(View):
    template_name = "pages/statuses.html"

    def get(self, request):
        return render(request, self.template_name, context={"statuses": Statuses.objects.all()})


class StatusesCreateView(View):
    template_name = "pages/statuses_create.html"

    def get(self, request, **kwargs):
        form = StatusCreateForm()
        return render(request, self.template_name, context={"form": form})
    
    def post(self, request, **kwargs):
        form = StatusCreateForm(request.POST or None)
        
        try:
            if form.is_valid():
                Statuses.objects.create(**form.cleaned_data)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Статус успешно создан",
                    fail_silently=True,
                )
                return redirect ('statuses')
        except Exception as error: 
            messages.add_message(
                request,
                messages.ERROR,
                error.message,
                fail_silently=True,
            )
        return redirect('statuses')
    
class StatusesUpdateView(View):
    template_name = "pages/statuses_update.html"

    def get(self, request, **kwargs):
        form = StatusCreateForm()
        return render(request, self.template_name, context={"form": form, "status": Statuses.objects.get(id=kwargs["pk"])})

    def post(self, request, **kwargs):
        form = StatusCreateForm(request.POST or None)
        get_new_value = request.POST.get('results')
        
        try:
            Statuses.objects.filter(id=kwargs["pk"]).update(name=get_new_value) #.update(name=request.name)
            messages.add_message(
                request,
                messages.SUCCESS,
                'Статус успешно обновлен',
                fail_silently=True,
            )

        except Exception as error: 
            messages.add_message(
                request,
                messages.ERROR,
                error,
                fail_silently=True,
            )
        return redirect('statuses')


class StatusesDeleteView(View):
    template_name = "pages/statuses_delete.html"

    def get(self, request, **kwargs):
        return render(request, self.template_name, context={"status": Statuses.objects.get(id=kwargs["pk"])})

    def post(self, request, **kwargs):
        try:
            status = Statuses.objects.get(id=kwargs["pk"])
            status.delete()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Статус успешно удален",
                fail_silently=True,
            )
        except Exception as error: 
            messages.add_message(
                request,
                messages.ERROR,
                error,
                fail_silently=True,
            )
        return redirect('statuses')