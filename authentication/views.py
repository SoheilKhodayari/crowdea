# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def getLogin(request):
	return render(request, "authentication/login.html", {})

def postLogin(request):
	username = request.POST["email"]
	password = request.POST["password"]

	return HttpResponse(username + password)

def getRegister(request):
	return render(request, "authentication/register.html", {})

def postRegister(request):
	pass