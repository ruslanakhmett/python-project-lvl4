import django_filters
from .models import Tasks
from django.contrib.auth.models import User
from django import forms
from .models import Statuses, Tasks, Labels

class TasksFilter(django_filters.FilterSet):
    #admin_id = User.objects.get(username='admin').id
    #self_tasks = django_filters.filters.BooleanFilter(queryset=Tasks.objects.all(), field_name='creator', widget=forms.CheckboxInput)
    labels = django_filters.ModelChoiceFilter(queryset=Labels.objects.all())
    perfomer = django_filters.ModelChoiceFilter(queryset=User.objects.all().exclude(is_superuser=True))
    class Meta:
        model = Tasks
        fields = ('status', 'perfomer', 'labels')