import django_filters
from .models import Tasks
from django.contrib.auth.models import User
from django import forms
from .models import Statuses, Tasks, Labels

class TasksFilter(django_filters.FilterSet):
    labels = django_filters.ModelChoiceFilter(queryset=Labels.objects.all())
    perfomer = django_filters.ModelChoiceFilter(queryset=User.objects.all().exclude(is_superuser=True))
    class Meta:
        model = Tasks
        fields = ('status', 'perfomer', 'labels')