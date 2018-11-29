# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.http import require_GET
from .models import Campaign
from django.http import Http404 
from django.http import HttpResponseNotFound


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




