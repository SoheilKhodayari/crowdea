# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# @Note: This model extends the Django User Model
# @Usage: Access this model only through User Model
#         user = User.objects.get(pk=user_id)
#         user.profile.bio = 'Lorem ipsum dolor sit amet'
#         user.save()
#
#     Useful User Fields:
#         - username
#         - password
#         - first_name
#         _ last_name
#         - last_login
#         - date_joined

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    short_bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
