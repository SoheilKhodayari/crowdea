# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse_lazy
from crowdea.utility import reverse_with_query
from django.core.exceptions import ObjectDoesNotExist
from idea.models import Idea
from datetime import datetime
from campaign.forms import PostForm
from .models import Campaign

# Create your views here.

def getOnAddCampaignSuccessUrl():
	kwargs = {"Msg": "Created-Successfully"}
	url_return_on_success = reverse_with_query("crowdeaApp:index", kwargs)
	return url_return_on_success

def postCampaign(request):
	if request.method == 'POST':
		campaign = PostForm(request.POST)
		if campaign.is_valid():
			campaign.save()
			return HttpResponseRedirect('/index.html')
		else:
			print("Invalid" + str(campaign.errors))
			return render(request, "campaign/add-campaign.html", {'form':campaign})
	else:
		idea = request.GET.get("idea")
		idea_obj = Idea.objects.get(pk=idea)
		form = PostForm(initial={'idea_ref':idea_obj})
		return render(request, 'campaign/add-campaign.html', {'form':form})
"""
	idea = request.POST.get("idea", "")
    # campaign_desc = request.POST.get("desc", "")
    # campaign_target = request.POST.get("c_target", "")
	# campaign_deadline = request.POST.get("c_deadline","")
	
	# if idea == "":
    # 	kwargs = {"Msg": "Error-Invalid-Idea"}
    # 	url_return_on_failure = reverse_with_query("ideaApp:getAddCampaign", kwargs)
	# 	return HttpResponseRedirect(url_return_on_failure)

	# if campaign_desc == "":
    # 	kwargs = {"Msg": "Error-Invalid-Desc"}
    # 	url_return_on_failure = reverse_with_query("ideaApp:getAddCampaign", kwargs)
	# 	return HttpResponseRedirect(url_return_on_failure)
		
	# if campaign_target == "":
    # 	kwargs = {"Msg": "Error-Invalid-Target"}
    # 	url_return_on_failure = reverse_with_query("ideaApp:getAddCampaign", kwargs)
	# 	return HttpResponseRedirect(url_return_on_failure)
		
	# if deadline == "":
    # 	kwargs = {"Msg": "Error-Invalid-Deadline"}
    # 	url_return_on_failure = reverse_with_query("ideaApp:getAddCampaign", kwargs)
	# 	return HttpResponseRedirect(url_return_on_failure)

	# try:
    #     ideaobj = idea.objects.get(id=idea)
	# 	c_deadline = datetime.strptime("%Y-%m-%d", campaign_deadline)
	# 	c_target = int(campaign_target)
	# 	c_instance = campaign.create(request.user, ideaobj, 
	# 		campaign_desc, campaign_target, c_deadline):
	# 	c_instance.save()
	# 	return HttpResponseRedirect(getOnAddCampaignSuccessUrl())
    # except ObjectDoesNotExist:
    #     kwargs = {"Msg": "Error-Invalid-Idea"}
    # 	url_return_on_failure = reverse_with_query("ideaApp:getAddCampaign", kwargs)
	# 	return HttpResponseRedirect(url_return_on_failure)
	# except TypeError:
	# 	kwargs = {"Msg": "Error-Invalid-Deadline"}
    # 	url_return_on_failure = reverse_with_query("ideaApp:getAddCampaign", kwargs)
	# 	return HttpResponseRedirect(url_return_on_failure)
	# except ValueError:
	# 	kwargs = {"Msg": "Error-Invalid-Target"}
	# 	url_return_on_failure = reverse_with_query("ideaApp:getAddCampaign", kwargs)
	# 	return HttpResponseRedirect(url_return_on_failure)
	# except ValidationError:
	# 	kwargs = {"Msg": "Error-Invalid-Target-Date"}
	# 	url_return_on_failure = reverse_with_query("ideaApp:getAddCampaign", kwargs)
	# 	return HttpResponseRedirect(url_return_on_failure)"""
