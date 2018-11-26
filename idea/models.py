# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Idea(models.Model):
	
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300, blank=True, null= True)
    idea = models.TextField(max_length=500, blank=True, null= True)
    is_active = models.BooleanField(default=True)
    meta_created_at = models.DateTimeField(auto_now_add=True)
    meta_last_updated_at = models.DateTimeField(auto_now=True)
    

