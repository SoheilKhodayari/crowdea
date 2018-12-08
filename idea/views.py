# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.http import JsonResponse
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.http import require_POST, require_GET
from crowdea.utility import reverse_with_query
from .models import Idea, IdeaRank
from campaign.models import Campaign
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import json

@require_GET
def getAddIdea(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))
    return render(request, "idea/add-idea.html", {})

def getAddIdeaOnSuccessRedirectUrl():
    kwargs = {"Msg": "Created-Successfully"}
    url_return_on_success = reverse_with_query("ideaApp:getAllIdeas", kwargs)
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
        messages.success(request, "Idea was successfully added!")
        return_url = getAddIdeaOnSuccessRedirectUrl()
        return HttpResponseRedirect(return_url)

@login_required
def getEditIdea(request, ideaId):
    idea = get_object_or_404(Idea, pk=ideaId)
    return render(request, "idea/edit-idea.html", {"idea": idea})


@login_required
def postEditIdea(request, ideaId):
    idea = get_object_or_404(Idea, pk=ideaId)
    text = request.POST.get("idea-text", None)
    is_active = request.POST.get("is-active", "")
    if is_active=="on":
        active = True 
    else:
        active = False

    idea.is_active = active

    if text is not None:
        idea.idea = text
    idea.save()
    messages.success(request, "Idea was successfully edited!")
    return HttpResponseRedirect(reverse_lazy("ideaApp:getIdeaById", kwargs={"ideaId":ideaId}))

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
    ownsIdea = False
    campaignId = -1

    if idea.user.id == request.user.id :
        ownsIdea = True
        campaign = Campaign.objects.filter(user=request.user,idea_ref=idea) 
        if campaign.count() > 0:
            campaignId = campaign[0].id

    return render(request, "idea/view-idea.html", {'idea': idea,'ownsIdea': ownsIdea, 'campaignId': campaignId})

@require_POST
def postRankIdea(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))

    try:
        rank = int(request.POST.get("rank", 0))
        idea_id = int(request.POST.get("idea_id", None))
    except:
        return HttpResponseForbidden('<h1>403: Forbidden</h1>')
    
    if idea_id is None or rank not in set([-1, 1]):
        return HttpResponseForbidden('<h1>403: Forbidden</h1>')
    
    user = request.user
    try:
        idea = Idea.objects.get(id = idea_id)
    except:
        return HttpResponseForbidden('<h1>403: Forbidden</h1>')

    rank_instance = IdeaRank.objects.filter(user=user, idea=idea)
    if not rank_instance:
        rank_instance = IdeaRank.objects.create(user=user, idea=idea)
        rank_instance.save()
    else:
        rank_instance = rank_instance[0]

    old_rank = rank_instance.value
    new_rank = rank if old_rank != rank else 0 # If same vote as before -> Cancel previous vote
    rating_inc = new_rank - old_rank

    #Update DB
    idea.rating = idea.rating + rating_inc
    idea.save()
    rank_instance.value = new_rank
    rank_instance.save()

    return JsonResponse({'rank': new_rank, 'rating':idea.rating})

def getAllIdeaRanksForUser(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))

    user = request.user
    idea_ranks = IdeaRank.objects.filter(user=user)

    result = []
    for rank in idea_ranks:
        result.append({'idea_id':rank.idea.id, 'rank': rank.value})

    return JsonResponse({'ranks': result})

def getIdeaRankForUser(request, idea_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))

    user = request.user
    idea = Idea.objects.get(id = idea_id)
    if idea is None:
        return HttpResponseForbidden('<h1>403: Forbidden</h1>')

    rank_instance = IdeaRank.objects.filter(user=user, idea=idea)
    rank = 0
    if rank_instance:
        rank = rank_instance[0].value

    return JsonResponse({'rank': rank})

