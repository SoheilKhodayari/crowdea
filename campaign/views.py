# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.decorators.http import require_GET
from .models import Campaign


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
		
	campaign = Campaign.objects.get(id=id)
	return render(request, "campaign/view-campaign.html", {'campaign': campaign})




