# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import User
from crowdea.utility import reverse_with_query
from .models import Idea, Comment
import json

class CommentTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
        username='testuser', password='1X<ISRUkw+tuK')
        self.test_user.save()
        login = self.client.login(
        username='testuser', password='1X<ISRUkw+tuK')

    def test_add_comment_successful(self):
        ideaInstance = Idea.objects.create(title="title", idea="idea",
                                           is_active=True, user=self.test_user)
        ideaInstance.save()
        # saving comment
        add_comment_endpoint = reverse("commentApp:postComment")
        response = self.client.post(add_comment_endpoint,
                                    {'idea_id': ideaInstance.id, 'comment': 'some fancy text'}	,
                                    follow=True)
        self.assertEqual(response.status_code, 200)

    def test_add_comment_invalid_idea(self):
        # saving comment
        add_comment_endpoint = reverse("commentApp:postComment")
        response = self.client.post(add_comment_endpoint,
                                    {'idea_id': -1, 'comment': 'some fancy text'}	,
                                    follow=True)
        self.assertEqual(response.status_code, 403)

    def test_add_empty_comment(self):
        ideaInstance = Idea.objects.create(title="title", idea="idea",
                                           is_active=True, user=self.test_user)
        ideaInstance.save()
        # saving comment
        add_comment_endpoint = reverse("commentApp:postComment")
        response = self.client.post(add_comment_endpoint,
                                    {'idea_id': ideaInstance.id},
                                    follow=True)
        self.assertEqual(response.status_code, 403)

    def testGetComments(self):
        ideaInstance = Idea.objects.create(title="title", idea="idea",
                                           is_active=True, user=self.test_user)
        ideaInstance.save()
        commentInstance = Comment.objects.create(comment="text",
                                                 idea=ideaInstance, user=self.test_user)
        commentInstance.save()
        commentInstance2 = Comment.objects.create(comment="text2",
                                                 idea=ideaInstance, user=self.test_user)
        commentInstance2.save()
        #getting comments:
        get_comments_endpoint = reverse("commentApp:getCommentsByIdeaId")
        response = self.client.get(get_comments_endpoint,
                                    {'idea_id': ideaInstance.id},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(len(response['comments']), 2)
