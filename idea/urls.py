"""testserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^get-add-idea$', views.getAddIdea, name="getAddIdea"),
    url(r'^add-idea$', views.postAddIdea, name="postAddIdea"),
    url(r'^get-all-ideas$', views.getAllIdeas, name="getAllIdeas"),
    url(r'^get-idea/(?P<ideaId>\d+)/$', views.getIdeaById, name="getIdeaById"),
    url(r'^get-filter-ideas$', views.getFilterIdeas, name="getFilterIdeas"),
    url(r'^get-filtered-ideas(?P<keyword>\w+|)$', views.getFilteredIdeas, name="getFilteredIdeas"),
    url(r'^rank-idea$', views.postRankIdea, name="postRankIdea"),
    url(r'^get-idea-ranks-for-user$', views.getAllIdeaRanksForUser, name="getAllIdeaRanksForUser"),
    url(r'^get-idea-rank-for-user/(?P<idea_id>\d+)/$', views.getIdeaRankForUser, name="getIdeaRankForUser")
]
