# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse_lazy
from crowdea.utility import reverse_with_query

# Create your views here.

def getLogin(request):
	return render(request, "authentication/login.html", {})

@require_POST
def postLogin(request):
	username = request.POST["email"]
	password = request.POST["password"]

	return HttpResponse(username + password)

def getRegister(request):
	return render(request, "authentication/register.html", {})

@require_POST
def postRegister(request):

	username = request.POST.get("username", "")
	password = request.POST.get("password", "")
	firstname = request.POST.get("firstname", "")
	lastname = request.POST.get("lastname", "")

	if username == "" or password == "" or firstname == "" or lastname == "":
		query_kwargs = {"Reg-Msg":"Incomplete-Data"}
		return HttpResponseRedirect(reverse_with_query("authApp:getRegister",query_kwargs))
	
	user, created = User.objects.get_or_create(username=username)
	if created:
		user.set_password(password)
		user.first_name = firstname
		user.last_name = lastname
		user.save()
		query_kwargs = {"Reg-Msg":"Successful"}
		return HttpResponseRedirect(reverse_with_query("index",query_kwargs))
	else:
		query_kwargs = {"Reg-Msg":"Error-Username-Exists"}
		return HttpResponseRedirect(reverse_with_query("authApp:getRegister", query_kwargs))	





