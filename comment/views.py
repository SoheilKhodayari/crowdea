# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse_lazy
from crowdea.utility import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST, require_GET
from idea.models import Idea
from datetime import datetime
from campaign.forms import PostForm
from .models import Comment
from django.http import Http404
from django.http import HttpResponseNotFound
from django.contrib import messages


@require_POST
def postComment(request):
    print("Hello World!!!!")

def getCommentsByIdeaId(request, id):
    print("Hello World!!!!!!!!!!!!!!!!!!!!!")
