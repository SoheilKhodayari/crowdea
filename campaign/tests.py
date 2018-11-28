# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your tests here.
class CampaignTest(TestCase):

    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_view_campaigns_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/campaigns')
        self.assertEqual(response.status_code, 200)

    def test_view_campaigns_url_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("campaignApp:getAllCampaigns"))
        self.assertEqual(response.status_code, 200)

    def test_view_campaigns_url_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("campaignApp:getAllCampaigns"))
        self.assertTemplateUsed(response, 'campaign/view-campaigns.html')   

    def test_view_campaigns_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("campaignApp:getAllCampaigns"))
        self.assertRedirects(response, reverse("authApp:getLogin"))
        