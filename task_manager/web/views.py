from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView, ListView

from .forms import SignUpForm, UserLoginForm, StatusCreateForm, LabelCreateForm
from .models import Statuses, Tasks, Labels
from .filters import TasksFilter
from .utils import is_auth




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

    def post(self, request, **kwargs):
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

        task = Tasks.objects.filter(perfomer_id=request.user.id)
        if task.exists():
            messages.add_message(
                request,
                messages.ERROR,
                'Невозможно удалить пользователя, потому что он используется',
                fail_silently=True)
            return redirect('users')

        else:
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
        context = {"statuses": Statuses.objects.all()}
        return is_auth(self.template_name, request, context)


class StatusesCreateView(View):
    template_name = "pages/statuses_create.html"

    def get(self, request):
        context = {"form": StatusCreateForm()}
        return is_auth(self.template_name, request, context)

    def post(self, request):
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
        context = {"form": StatusCreateForm(), 
                   "status": Statuses.objects.get(id=kwargs["pk"])}
        return is_auth(self.template_name, request, context)


    def post(self, request, **kwargs):

        try:
            Statuses.objects.filter(id=kwargs["pk"]).update(name=request.POST.get('results')) #.update(name=request.name)
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
        context = {"status": Statuses.objects.get(id=kwargs["pk"])}
        return is_auth(self.template_name, request, context)

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


class TasksListView(ListView):
    template_name = "pages/tasks.html"
    model = Tasks

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.GET.get('self_tasks') == 'on':
            queryset = self.get_queryset().filter(creator_id=self.request.user.pk)
        else:
            queryset = self.get_queryset()

        context['filter'] = TasksFilter(self.request.GET, queryset=queryset)
        return context


class TasksCreateView(View):
    template_name = "pages/tasks_create.html"
    
    def get(self, request, **kwargs):
        context = {"users": User.objects.all().exclude(username="admin"),
                   "statuses": Statuses.objects.all(),
                   "labels": Labels.objects.all()}
        return is_auth(self.template_name, request, context)

    def post(self, request, **kwargs):

        if request.user.is_authenticated:
            get_name = request.POST.get('name')
            get_text = request.POST.get('text')
            get_perfomer_id = User.objects.get(username=request.POST.get('perfomer')).id
            get_status_id = Statuses.objects.get(name=request.POST.get('status')).id
            get_labels_list = request.POST.getlist('labels')
            
            labels_id_list = []
            for name in get_labels_list:
                labels_id_list.append(Labels.objects.get(name=name).id)
            
            instance = Tasks.objects.create(
                name=get_name,
                description=get_text,
                perfomer_id=get_perfomer_id,
                status_id=get_status_id,
                creator_id=request.user.pk,

            )
            instance.labels.add(*labels_id_list)  # add m2m data

            messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Задача успешно создана.",
                    fail_silently=True,
                )
            return redirect("tasks")


class TasksUpdateView(View):
    template_name = "pages/tasks_update.html"

    def get(self, request, **kwargs):

        context = {"task": Tasks.objects.get(id=kwargs["pk"]),
                   "users": User.objects.all().exclude(username="admin"),
                   "statuses": Statuses.objects.all(),
                   "all_labels": Labels.objects.all(),
                   "used_labels": Tasks.objects.get(id=kwargs["pk"]).labels.all()}
        return is_auth(self.template_name, request, context)


    def post(self, request, **kwargs):

        if request.user.is_authenticated:
            get_name = request.POST.get('name')
            get_text = request.POST.get('text')
            get_perfomer_id = User.objects.get(username=request.POST.get('perfomer')).id
            get_status_id = Statuses.objects.get(name=request.POST.get('status')).id
            get_labels_list = request.POST.getlist('labels')
            
            labels_id_list = []
            for name in get_labels_list:
                labels_id_list.append(Labels.objects.get(name=name).id)

            try:
                Tasks.objects.filter(id=kwargs["pk"]).update(
                    name=get_name,
                    description=get_text,
                    perfomer_id=get_perfomer_id,
                    status_id=get_status_id,
                    )
                
                instance = Tasks.objects.get(id=kwargs["pk"])
                instance.labels.set(labels_id_list)  # update m2m data from list

                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Задача успешно обновлена',
                    fail_silently=True,
                )
                return redirect("tasks")
                

            except Exception as error: 
                messages.add_message(
                    request,
                    messages.ERROR,
                    error,
                    fail_silently=True,
                )
            return redirect("tasks")

        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Вы не авторизованы! Пожалуйста, выполните вход.",
                fail_silently=True,
            )
            return redirect("login")


class TasksDeleteView(View):
    template_name = "pages/tasks_delete.html"

    def get(self, request, **kwargs):
        task = Tasks.objects.get(id=kwargs["pk"])
        
        if request.user.is_authenticated and request.user.pk == task.creator_id:
            return render(request,
                        self.template_name,
                        context={"task": Tasks.objects.get(id=kwargs["pk"])})
        else:
            messages.add_message(
                request,
                messages.ERROR,
                "Задачу может удалить только её автор",
                fail_silently=True,
            )
            return redirect('tasks')

    def post(self, request, **kwargs):
        task = Tasks.objects.get(id=kwargs["pk"])
        if request.user.is_authenticated and request.user.pk == task.creator_id:
            try:
                task.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Задача успешно удалена",
                    fail_silently=True,
                )

            except Exception as error: 
                messages.add_message(
                    request,
                    messages.ERROR,
                    error,
                    fail_silently=True,
                )
            return redirect('tasks')


class TaskDetailsShowView(View):
    template_name = "pages/task_show.html"

    def get(self, request, **kwargs):
        context = {"task": Tasks.objects.get(id=kwargs["pk"])}
        return is_auth(self.template_name, request, context)


class LabelsView(View):
    template_name = "pages/labels.html"

    def get(self, request):
        context = {"labels": Labels.objects.all()}
        return is_auth(self.template_name, request, context)


class LabelsCreateView(View):
    template_name = "pages/labels_create.html"

    def get(self, request):
        context = {"form": LabelCreateForm()}
        return is_auth(self.template_name, request, context)


    def post(self, request, **kwargs):
        form = LabelCreateForm(request.POST or None)
        
        try:
            if form.is_valid():
                Labels.objects.create(**form.cleaned_data)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Метка успешно создана",
                    fail_silently=True,
                )
                return redirect ('labels')
        except Exception as error: 
            messages.add_message(
                request,
                messages.ERROR,
                error.message,
                fail_silently=True,
            )
        return redirect('labels')
    
    
class LabelsUpdateView(View):
    template_name = "pages/labels_update.html"

    def get(self, request, **kwargs):
        context = {"form": LabelCreateForm(), 
                   "label": Labels.objects.get(id=kwargs["pk"])}
        return is_auth(self.template_name, request, context)

    def post(self, request, **kwargs):

        try:
            Labels.objects.filter(id=kwargs["pk"]).update(name=request.POST.get('results'))
            messages.add_message(
                request,
                messages.SUCCESS,
                'Метка успешно обновлена',
                fail_silently=True,
            )

        except Exception as error: 
            messages.add_message(
                request,
                messages.ERROR,
                error,
                fail_silently=True,
            )
        return redirect('labels')


class LabelsDeleteView(View):
    template_name = "pages/labels_delete.html"

    def get(self, request, **kwargs):
        context = {"label": Labels.objects.get(id=kwargs["pk"])}
        return is_auth(self.template_name, request, context)

    def post(self, request, **kwargs):

        try:
            label = Labels.objects.get(id=kwargs["pk"])

            if not label.tasks_set.exists():
                label.delete()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Метка успешно удалена",
                    fail_silently=True,
                )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Невозможно удалить метку, потому что она используется",
                    fail_silently=True)
                redirect('labels')

        except Exception as error: 
            messages.add_message(
                request,
                messages.ERROR,
                error,
                fail_silently=True,
            )
        return redirect('labels')