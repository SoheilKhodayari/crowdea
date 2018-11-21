# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.core.urlresolvers import reverse_lazy
from crowdea.utility import reverse_with_query


def index(request):
	context_vars = {}
	if request.user.is_authenticated():
		context_vars["user"]=  request.user
	return render(request, 'index.html', context_vars)

