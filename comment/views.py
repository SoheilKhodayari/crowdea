# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
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
from django.http import JsonResponse

@require_POST
def postComment(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))

    comment = request.POST.get("comment", None)
    idea_id = int(request.POST.get("idea_id", None))
    user = request.user
    try:
        idea = Idea.objects.get(id=idea_id)
    except:
        return HttpResponseForbidden('<h1>403: Forbidden</h1>')

    Comment.objects.create(comment=comment, user=user, idea=idea)
    return JsonResponse({})

def getCommentsByIdeaId(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))
    print("meh!")
    idea_id = int(request.GET.get("idea_id", None))
    print(idea_id)
    idea = Comment.objects.get(id=idea_id)
    comments = Comment.objects.get(idea)
    return JsonResponse({'comments': comments})
