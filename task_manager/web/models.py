from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _



class Statuses(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Labels(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Tasks(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length = 1000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, related_name='status', blank=True, verbose_name=_('Статус'))
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', blank=True)
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executor_id', default='None', blank=True, verbose_name=_('Исполнитель'))
    labels = models.ManyToManyField(Labels, verbose_name=_('Метка'))
    
    def __str__(self):
        return self.name





#for extend user profile:

# from django.db.models.signals import post_save
# from django.dispatch import receiver


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = ...

# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()
