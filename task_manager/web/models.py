from django.db import models
from django.contrib.auth.models import User
























# from django.db.models.signals import post_save
# from django.dispatch import receiver


#for extend user profile:

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     avatar = ...


#     def __str__(self):
#         return self.user.username


# @receiver(post_save, sender=User)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()