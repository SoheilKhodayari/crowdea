# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import User
from crowdea.utility import reverse_with_query
from .views import getAddIdeaOnSuccessRedirectUrl

# Create your tests here.


class IdeaTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            username='testuser', password='1X<ISRUkw+tuK')
        self.test_user.save()

        login = self.client.login(
            username='testuser', password='1X<ISRUkw+tuK')

    def test_add_idea_successful(self):
        add_idea_endpoint = reverse("ideaApp:postAddIdea")
        response = self.client.post(add_idea_endpoint,
		{'idea-title': 'testIdea', 'idea-text': 'idea content', 'user': self.test_user, 'is_active': 'on'}		, follow=True)

        self.assertEqual(response.status_code, 200)

        success_url = getAddIdeaOnSuccessRedirectUrl()
        self.assertRedirects(response, success_url)

    def test_add_idea_failure(self):
	add_idea_endpoint = reverse("ideaApp:postAddIdea")
        response = self.client.post(add_idea_endpoint, 
            {'idea-title': 'testIdea', 'idea-text': '', 'user': self.test_user, 'is_active': 'on'}
            , follow=True)
        self.assertEqual(response.status_code, 200)

        kwargs = {"Msg": "Error-Invalid-Data"}
        failure_url = reverse_with_query("ideaApp:getAddIdea", kwargs)
        self.assertRedirects(response, failure_url)


