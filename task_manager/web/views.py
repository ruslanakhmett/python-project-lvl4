from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import CreateView, ListView
from django.utils.translation import gettext_lazy as _

from .forms import (
    SignUpForm,
    UserLoginForm,
    StatusCreateForm,
    LabelCreateForm,
    TaskCreateForm,
)
from .models import Statuses, Tasks, Labels
from .filters import TasksFilter
from .utils import CustomLoginRequiredMixin


class IndexView(View):
    def get(self, request):
        return render(request, "pages/index.html")


class LogoutView(View):
    def post(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, _("Вы разлогинены"))
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
                messages.add_message(request, messages.SUCCESS, _("Вы залогинены"))
                return redirect("index")
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _(
                        "Пожалуйста, введите правильные имя пользователя и пароль. \
                                         Оба поля могут быть \
                                             чувствительны к регистру."
                    ),
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
                request, messages.SUCCESS, _("Пользователь успешно зарегистрирован")
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


class UpdateUserView(CustomLoginRequiredMixin, View):
    template_name = "pages/user_update.html"

    def get(self, request, **kwargs):
        form = SignUpForm(instance=request.user)

        user_id_from_link = kwargs["pk"]
        if request.user.pk == user_id_from_link:
            return render(request, self.template_name, context={"form": form})
        messages.add_message(
            request,
            messages.ERROR,
            _("У вас нет прав для изменения другого пользователя."),
            fail_silently=True,
        )
        return redirect("users")

    def post(self, request, **kwargs):
        form = SignUpForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, _("Пользователь успешно изменён")
            )
            return redirect("users")
        return render(request, self.template_name, context={"form": form})


class DeleteUserView(CustomLoginRequiredMixin, View):
    template_name = "pages/user_delete.html"

    def get(self, request, **kwargs):

        user_id_from_link = kwargs["pk"]
        if request.user.id == user_id_from_link:
            return render(request, self.template_name)
        messages.add_message(
            request,
            messages.ERROR,
            _("У вас нет прав для изменения другого пользователя."),
            fail_silently=True,
        )
        return redirect("users")

    def post(self, request, **kwargs):

        task = Tasks.objects.filter(executor_id=request.user.id)
        if task.exists():
            messages.add_message(
                request,
                messages.ERROR,
                _("Невозможно удалить пользователя, потому что он используется"),
                fail_silently=True,
            )
            return redirect("users")

        else:
            try:
                user = User.objects.get(id=request.user.id)
                user.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Пользователь успешно удалён"),
                    fail_silently=True,
                )
            except Exception as error:
                messages.add_message(
                    request,
                    messages.ERROR,
                    error.message,
                    fail_silently=True,
                )
            return redirect("users")


class StatusesShowView(CustomLoginRequiredMixin, View):
    template_name = "pages/statuses.html"

    def get(self, request):
        context = {"statuses": Statuses.objects.all()}
        return render(request, self.template_name, context)


class StatusesCreateView(CustomLoginRequiredMixin, View):
    template_name = "pages/statuses_create.html"

    def get(self, request):
        context = {"form": StatusCreateForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = StatusCreateForm(request.POST or None)

        if form.is_valid():
            Statuses.objects.create(**form.cleaned_data)

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Статус успешно создан"),
                fail_silently=True,
            )
            return redirect("statuses")
        else:
            return render(request, self.template_name, {"form": form})


class StatusesUpdateView(View):
    template_name = "pages/statuses_update.html"

    def get(self, request, **kwargs):
        context = {
            "form": StatusCreateForm(),
            "status": Statuses.objects.get(id=kwargs["pk"]),
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        try:
            Statuses.objects.filter(id=kwargs["pk"]).update(
                name=request.POST.get("results")
            )  # .update(name=request.name)
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Статус успешно изменён"),
                fail_silently=True,
            )

        except Exception as error:
            messages.add_message(
                request,
                messages.ERROR,
                error,
                fail_silently=True,
            )
        return redirect("statuses")


class StatusesDeleteView(CustomLoginRequiredMixin, View):
    template_name = "pages/statuses_delete.html"

    def get(self, request, **kwargs):
        context = {"status": Statuses.objects.get(id=kwargs["pk"])}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        try:
            status = Statuses.objects.get(id=kwargs["pk"])

            if not Tasks.objects.filter(status_id=kwargs["pk"]):
                status.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Статус успешно удалён"),
                    fail_silently=True,
                )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _("Невозможно удалить статус, потому что он используется"),
                    fail_silently=True,
                )
                redirect("labels")

        except Exception as error:
            messages.add_message(
                request,
                messages.ERROR,
                error,
                fail_silently=True,
            )
        return redirect("statuses")


class TasksListView(CustomLoginRequiredMixin, ListView):
    template_name = "pages/tasks.html"
    model = Tasks

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.GET.get("self_tasks"):
            queryset = self.get_queryset().filter(creator_id=self.request.user.pk)
        else:
            queryset = self.get_queryset()

        context["filter"] = TasksFilter(self.request.GET, queryset=queryset)

        return context


class TasksCreateView(CustomLoginRequiredMixin, View):
    template_name = "pages/tasks_create.html"

    def get(self, request, **kwargs):

        context = {
            "form": TaskCreateForm()}

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = TaskCreateForm(request.POST or None)

        if form.is_valid():
            name = request.POST.get("name")
            description = request.POST.get("description")
            status_id = request.POST.get("status")
            executor_id = request.POST.get("executor") if request.POST.get("executor") else None
            labels_id_list = request.POST.getlist("labels") if request.POST.getlist("labels") else []

            Tasks.objects.create(
                name=name,
                description=description,
                status_id=status_id,
                executor_id=executor_id,
                creator_id=request.user.pk).labels.add(*labels_id_list)  # add m2m data

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Задача успешно создана"),
                fail_silently=True,
            )
            return redirect("tasks")
        else:
            return render(request, self.template_name, {"form": form})


class TasksUpdateView(CustomLoginRequiredMixin, View):
    template_name = "pages/tasks_update.html"

    def get(self, request, **kwargs):

        instance = Tasks.objects.get(id=kwargs['pk'])

        context = {
            "form": TaskCreateForm(instance=instance)
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        instance = get_object_or_404(Tasks, id=kwargs['pk'])
        form = TaskCreateForm(request.POST or None, instance=instance)

        if form.is_valid():
            form.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Задача успешно изменена"),
                fail_silently=True,
            )
            return redirect("tasks")

        return redirect("tasks")


class TasksDeleteView(CustomLoginRequiredMixin, View):
    template_name = "pages/tasks_delete.html"

    def get(self, request, **kwargs):
        task = Tasks.objects.get(id=kwargs["pk"])

        if request.user.is_authenticated and request.user.pk == task.creator_id:
            return render(
                request,
                self.template_name,
                context={"task": Tasks.objects.get(id=kwargs["pk"])},
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                _("Задачу может удалить только её автор"),
                fail_silently=True,
            )
            return redirect("tasks")

    def post(self, request, **kwargs):
        task = Tasks.objects.get(id=kwargs["pk"])
        if request.user.is_authenticated and request.user.pk == task.creator_id:
            try:
                task.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Задача успешно удалена"),
                    fail_silently=True,
                )

            except Exception as error:
                messages.add_message(
                    request,
                    messages.ERROR,
                    error,
                    fail_silently=True,
                )
            return redirect("tasks")


class TaskDetailsShowView(CustomLoginRequiredMixin, View):
    template_name = "pages/task_show.html"

    def get(self, request, **kwargs):
        context = {"task": Tasks.objects.get(id=kwargs["pk"])}
        return render(request, self.template_name, context)


class LabelsView(CustomLoginRequiredMixin, View):
    template_name = "pages/labels.html"

    def get(self, request):
        context = {"labels": Labels.objects.all()}
        return render(request, self.template_name, context)


class LabelsCreateView(CustomLoginRequiredMixin, View):
    template_name = "pages/labels_create.html"

    def get(self, request, **kwargs):
        context = {"form": LabelCreateForm()}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = LabelCreateForm(request.POST or None)

        if form.is_valid():
            Labels.objects.create(**form.cleaned_data)

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Метка успешно создана"),
                fail_silently=True,
            )
            return redirect("labels")
        else:
            return render(request, self.template_name, {"form": form})


class LabelsUpdateView(CustomLoginRequiredMixin, View):
    template_name = "pages/labels_update.html"

    def get(self, request, **kwargs):
        context = {
            "form": LabelCreateForm(),
            "label": Labels.objects.get(id=kwargs["pk"]),
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        try:
            Labels.objects.filter(id=kwargs["pk"]).update(
                name=request.POST.get("results")
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                _("Метка успешно изменена"),
                fail_silently=True,
            )

        except Exception as error:
            messages.add_message(
                request,
                messages.ERROR,
                error,
                fail_silently=True,
            )
        return redirect("labels")


class LabelsDeleteView(CustomLoginRequiredMixin, View):
    template_name = "pages/labels_delete.html"

    def get(self, request, **kwargs):
        context = {"label": Labels.objects.get(id=kwargs["pk"])}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        try:
            label = Labels.objects.get(id=kwargs["pk"])

            if not label.tasks_set.exists():
                label.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    _("Метка успешно удалена"),
                    fail_silently=True,
                )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    _("Невозможно удалить метку, потому что она используется"),
                    fail_silently=True,
                )
                redirect("labels")

        except Exception as error:
            messages.add_message(
                request,
                messages.ERROR,
                error,
                fail_silently=True,
            )
        return redirect("labels")
