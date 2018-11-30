# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.http import require_POST, require_GET
from crowdea.utility import reverse_with_query
from .models import Idea
from django.db.models import Q
import json

@require_GET
def getAddIdea(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))
	return render(request, "idea/add-idea.html", {})

def getAddIdeaOnSuccessRedirectUrl():
	kwargs = {"Msg": "Created-Successfully"}
	url_return_on_success = reverse_with_query("ideaApp:getAddIdea", kwargs)
	return url_return_on_success

@require_POST
def postAddIdea(request):
    title = request.POST.get("idea-title", "")
    idea_text = request.POST.get("idea-text", "")
    is_active = request.POST.get("is-active", "")

    if title == "" or idea_text == "":
    	kwargs = {"Msg": "Error-Invalid-Data"}
    	url_return_on_failure = reverse_with_query("ideaApp:getAddIdea", kwargs)
    	return HttpResponseRedirect(url_return_on_failure)

    else:
    	if is_active=="on":
    		active = True 
    	else:
    		active = False
    	ideaInstance = Idea.objects.create(title=title, idea=idea_text, 
    		is_active=active, user=request.user)
    	ideaInstance.save()

    	return_url = getAddIdeaOnSuccessRedirectUrl()
    	return HttpResponseRedirect(return_url)

def getFilterIdeas(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))
	return render(request, "idea/filter-ideas.html", {})

def getFilteredIdeas(request, keyword):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))
	print("Hello World!")
	# Disclaimer: this stuff does not work yet!
	if keyword and keyword.strip():
		ideas = Idea.objects.filter(Q(title__icontains=keyword)
                                          | Q(idea__icontains=keyword)).order_by('-meta_created_at')
	else:
		print("was here...")
		ideas = Idea.objects.all().order_by('-meta_created_at')
	print(ideas.__len__())
	# temporary thing, later json will be returned:
	return render(request, "idea/filter-ideas.html", {}) #json.dumps(ideas)

def getAllIdeas(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))
	ideas = Idea.objects.all().order_by('-meta_created_at')
	#print(ideas.__len__())
	return render(request, "idea/view-ideas.html", {'ideas': ideas})

def getIdeaById(request, ideaId):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))
	idea = Idea.objects.get(id = ideaId)
	return render(request, "idea/view-idea.html", {'idea': idea})