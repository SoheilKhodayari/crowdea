# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy


def index(request):
    # Redirect if user is not authenticated
    if not request.user.is_authenticated(): 
        return HttpResponseRedirect(reverse_lazy("authApp:getLogin"))

    context_vars = {"user": request.user}
    return render(request, 'index.html', context_vars)



def getLandingIndex(request):
	
	context_vars = {}
	if request.user.is_authenticated():
		context_vars["user"] =  request.user
	return render(request, "landing.html", context_vars)
