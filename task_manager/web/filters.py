import django_filters
from .models import Tasks, Labels, MyUser


class TasksFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(queryset=Labels.objects.all())
    executor = django_filters.ModelChoiceFilter(
        queryset=MyUser.objects.all().exclude(username="admin")
    )

    class Meta:
        model = Tasks
        fields = ["status", "executor", "labels"]
