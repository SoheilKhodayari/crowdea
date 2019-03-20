from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^add-comment$', views.postComment, name="postComment"),
    url(r'^comments$', views.getCommentsByIdeaId, name="getCommentsByIdeaId"),
]