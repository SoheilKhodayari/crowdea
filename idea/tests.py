# # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import User
from crowdea.utility import reverse_with_query
from .views import getAddIdeaOnSuccessRedirectUrl

# # Create your tests here.
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
                                    {'idea-title': 'testIdea', 'idea-text': 'idea content', 'user': self.test_user, 'is_active': 'on'}	,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        success_url = getAddIdeaOnSuccessRedirectUrl()
        self.assertRedirects(response, success_url)

    def test_add_idea_failure(self):
        add_idea_endpoint = reverse("ideaApp:postAddIdea")
        response = self.client.post(add_idea_endpoint,
                                    {'idea-title': 'testIdea', 'idea-text': '', 'user': self.test_user, 'is_active': 'on'},
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        kwargs = {"Msg": "Error-Invalid-Data"}
        failure_url = reverse_with_query("ideaApp:getAddIdea", kwargs)
        self.assertRedirects(response, failure_url)

    def test_view_ideas_success(self):
        # adding 2 ideas first:
        add_idea_endpoint = reverse("ideaApp:postAddIdea")
        idea1 = {'idea-title': 'testIdea1', 'idea-text': 'idea content 1', 'user': self.test_user,
                          'is_active': 'on'}
        idea2 = {'idea-title': 'testIdea2', 'idea-text': 'idea content 2', 'user': self.test_user,
                 'is_active': 'off'}
        self.client.post(add_idea_endpoint, idea1, follow=True)
        self.client.post(add_idea_endpoint, idea2, follow=True)
        # now getting ideas:
        view_ideas_endpoint = reverse("ideaApp:getAllIdeas")
        response = self.client.get(view_ideas_endpoint)
        # checking http status:
        self.assertEqual(response.status_code, 200)
        # checking list size and contents. newest idea should come first:
        ideas_list = response.context['ideas']
        self.assertEqual(ideas_list.__len__(), 2)
        self.assertEqual(ideas_list[0].title, 'testIdea2')
        self.assertEqual(ideas_list[0].idea, 'idea content 2')
        self.assertEqual(ideas_list[0].user, self.test_user)
        self.assertEqual(ideas_list[0].is_active, False)

    def test_view_idea_success(self):
        # adding idea first:
        add_idea_endpoint = reverse("ideaApp:postAddIdea")
        self.client.post(add_idea_endpoint,
                         {'idea-title': 'testIdea', 'idea-text': 'idea content', 'user': self.test_user,
                          'is_active': 'on'}, follow=True)
        # TODO: problem here. how can I get the id of a freshly generated idea?
        #   --->> ANSWER: you need to create a fake idea (say ideaInstance) in setUp method, then id = ideaInstance.pk
        # viewing idea now:
        # TODO: problem here. please, help with getting the endpoint. these attempts didn't work
        #view_idea_endpoint = reverse("ideaApp:getIdeaById", id=1)
        # ---->> ANSWER: the way you pass it should be like below: remember that the slug name "ideaId" is defined in urls.py 
        view_idea_endpoint = reverse("ideaApp:getIdeaById", kwargs={'ideaId':1})
        #response = self.client.get(view_idea_endpoint)
        # checking http status
        #self.assertEqual(response.status_code, 200)