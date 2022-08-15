from django.contrib.auth.models import User
from django.db import models




class Statuses(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Labels(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Tasks(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length = 1000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Statuses, on_delete=models.CASCADE, related_name='status', blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator', blank=True)
    perfomer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='perfomer', blank=True)
    labels = models.ManyToManyField(Labels)






# from django.db.models.signals import post_save
# from django.dispatch import receiver


#for extend user profile:

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = ...


# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()
