# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from idea.models import Idea

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null=False)
    meta_created_at = models.DateTimeField(auto_now_add=True)