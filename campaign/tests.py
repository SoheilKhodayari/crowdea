# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from idea.models import Idea
from .models import Campaign
from datetime import datetime

# Create your tests here.
class CampaignTest(TestCase):

    def setUp(self):
        # Create two users
        self.test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        self.test_user1.save()

        ideas_info = [
            {'title': 'New app for food delivery', 
             'is_active':True,
             'idea': 'incidunt non ac eros. Vestibulum ante '\
             'ipsum primis in faucibus orci luctus et ultrices'\
             'posuere cubilia urae; Sed convallis, leo at'\
             'fringilla faucibus, ante purus tempus libero, non'\
             'ravida elit sapien a mi. Aliquam laoreet, dui'\
             'pulvinar tempus efficitur, sapien ci placerat'\
             'enim, it amet fringilla risus risus et lectus.',
             'meta_created_at': '05/08/2018',
             'meta_last_updated_at': '11/10/2018'},
            {'title': 'The perfect ecommerce website', 
             'is_active':True,
             'idea': 'Lorem ipsum dolor sit amet, consectetur' \
             'adipiscing elit. Nam blandit suscipit massa quis' \
             'pharetra. Aliquam aliquam pretium consectetur.' \
             'Sed lorem sapien, blandit sed suscipit id,' \
             'tristique sed tellus. Integer elementum pharetra ' \
             'odio eu vestibulum. Aenean et neque et mi aliquet ',
             'meta_created_at': '05/10/2018',
             'meta_last_updated_at': '25/11/2018'}]
        self.ideas = self._create_ideas(ideas_info, self.test_user1)

        campaigns_info = [
            {'idea': 0,
             'description': 'Integer pellentesque ornare' \
             ' diam, id blandit neque dictum sit amet. Etiam' \
             ' ultrices est ac lorem commodo gravida. Phasellus' \
             ' scelerisque tortor tincidunt lacus ornare, a finibus' \
             ' turpis tristique. Donec tortor nisl, maximus ut'\
             'volutpat sit amet, sodales ut odio. ',
             'campaign_target_sum': 20000,
             'campaign_collected_sum': 200,
             'meta_created_at': '28/11/2018',
             'meta_campaign_deadline': '01/02/2019'},
            {'idea': 1,
             'description': 'Integer pellentesque ornare' \
             ' diam, id blandit neque dictum sit amet. Etiam' \
             ' ultrices est ac lorem commodo gravida. Phasellus' \
             ' scelerisque tortor tincidunt lacus ornare, a finibus' \
             ' turpis tristique. Donec tortor nisl, maximus ut'\
             'volutpat sit amet, sodales ut odio. ',
             'campaign_target_sum': 5000,
             'campaign_collected_sum': 4700,
             'meta_created_at': '23/10/2018',
             'meta_campaign_deadline': '31/12/2019'}]
        self.campaigns = self._create_campaigns(campaigns_info, self.ideas, self.test_user1)

    def _create_ideas(self, ideas_info, user):
        result = []
        for info in ideas_info:
            idea = Idea.objects.create(
                title=info['title'], 
                idea=info['idea'], 
                is_active=info['is_active'], 
                user=user,
                meta_created_at=datetime.strptime(info['meta_created_at'], '%d/%m/%Y'),
                meta_last_updated_at=datetime.strptime(info['meta_last_updated_at'], '%d/%m/%Y'))
            idea.save()
            result.append(idea)
        return result

    def _create_campaigns(self, campaigns_info, ideas, user):
        result = []
        for info in campaigns_info:
            campaign = Campaign.create(
                user=user,
                idea=ideas[info['idea']],
                description=info['description'],
                c_target=info['campaign_target_sum'],
                collected=info['campaign_collected_sum'],
                c_deadline=datetime.strptime(info['meta_campaign_deadline'], '%d/%m/%Y'))
            campaign.save()
            result.append(campaign)
        return result

    # Campaigns
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

    def test_view_campaigns_return_correct_data(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("campaignApp:getAllCampaigns"))

        campaigns = response.context['campaigns']
        self.assertEqual(len(campaigns), 2)
        self.assertEqual(campaigns[0].title, self.campaigns[0].title)
        self.assertEqual(campaigns[0].idea, self.campaigns[0].idea)
        self.assertEqual(campaigns[0].is_active, self.campaigns[0].is_active)
        self.assertEqual(campaigns[0].description, self.campaigns[0].description)
        self.assertEqual(campaigns[0].campaign_target_sum, self.campaigns[0].campaign_target_sum)
        self.assertEqual(campaigns[0].campaign_collected_sum, self.campaigns[0].campaign_collected_sum)
        
    # Campaign
    def test_view_campaign_url_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("campaignApp:getCampaignById", 
                                            kwargs={'id':self.campaigns[0].id}))
        self.assertEqual(response.status_code, 200)

    def test_view_campaign_url_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("campaignApp:getCampaignById", 
                                            kwargs={'id':self.campaigns[0].id}))
        self.assertTemplateUsed(response, 'campaign/view-campaign.html')  

    def test_view_campaign_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("campaignApp:getCampaignById", 
                                            kwargs={'id':self.campaigns[0].id}))
        self.assertRedirects(response, reverse("authApp:getLogin"))

    def test_view_campaign_return_correct_data(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("campaignApp:getCampaignById", 
                                            kwargs={'id':self.campaigns[0].id}))

        campaign = response.context['campaign']
        self.assertEqual(len(campaigns), 2)
        self.assertEqual(campaigns.title, self.campaigns[0].title)
        self.assertEqual(campaigns.idea, self.campaigns[0].idea)
        self.assertEqual(campaigns.is_active, self.campaigns[0].is_active)
        self.assertEqual(campaigns.description, self.campaigns[0].description)
        self.assertEqual(campaigns.campaign_target_sum, self.campaigns[0].campaign_target_sum)
        self.assertEqual(campaigns.campaign_collected_sum, self.campaigns[0].campaign_collected_sum)
        
    def test_view_campaign_return_correct_data(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("campaignApp:getCampaignById", 
                                            kwargs={'id':20}))

        self.assertEqual(response.status_code, 404)
 


        