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
from .models import Campaign
from django.http import Http404 
from django.http import HttpResponseNotFound
from django.contrib import messages

def getOnAddCampaignSuccessUrl(ideaId):
	kwargs = {"Msg": "Created-Successfully"}
	arg= {ideaId }
	url_return_on_success = reverse_with_query_args("campaignApp:getCampaignById", arg, kwargs)
	return url_return_on_success

def postCampaign(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))

	if request.method == 'POST':
		campaign = PostForm(request.POST)
		if campaign.is_valid():
			campaign_obj = campaign.save()
			id=campaign_obj.pk
			messages.success(request, "Campaign has started. Good luck!")
			return HttpResponseRedirect(getOnAddCampaignSuccessUrl(id))
		else:
			print("Invalid" + str(campaign.errors))
			return render(request, "campaign/add-campaign.html", {'form':campaign})
	else:
		idea = request.GET.get("idea")
		user = request.user
		idea_obj = Idea.objects.get(pk=idea)
		#Add 401 template with message - TOD
		if( idea_obj.user.id != user.id):
			return HttpResponseRedirect(reverse_lazy("getIdeaById"),{idea})
		form = PostForm(initial={'idea_ref':idea_obj, 'user': user, 'title': idea_obj.title, 
			'idea': idea_obj.idea, 'is_active': idea_obj.is_active,'campaign_collected_sum': 0})
		return render(request, 'campaign/add-campaign.html', {'form':form})


@require_GET
def getAllCampaigns(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))

	campaigns = Campaign.objects.all()
	return render(request, "campaign/view-campaigns.html", {'campaigns': campaigns})

@require_GET
def getCampaignById(request, id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))
	
	try:
		campaign = Campaign.objects.get(id=id)
	except Exception as e:
		return HttpResponseNotFound('<h1>404: Campaign not found</h1>')

	return render(request, "campaign/view-campaign.html", {'campaign': campaign})