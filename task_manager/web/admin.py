from django.contrib import admin
from .models import Labels, Statuses, Tasks

admin.site.register(Labels)
admin.site.register(Statuses)
admin.site.register(Tasks)
