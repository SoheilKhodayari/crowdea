# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from idea.models import Idea
from campaign.utils import validate_campaign_target

class Campaign(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_id')
    idea_ref = models.ForeignKey(Idea, on_delete=models.PROTECT, related_name='idea_ref')
    title = models.CharField(max_length=300, blank=True, null= True)
    idea = models.TextField(max_length=500, blank=True, null= True)
    is_active = models.BooleanField(default=True)
    #Custom fields of campaign
    description = models.CharField(max_length=1000, blank=False, null=False)
    meta_created_at = models.DateTimeField(auto_now_add=True)
    campaign_target_sum = models.IntegerField(blank=False, null=False)
    campaign_collected_sum = models.IntegerField(default=0, blank=False, null=False)
    meta_campaign_deadline = models.DateTimeField(blank=False, null=False,validators=[validate_campaign_target])

    def __unicode__(self):
        return u'%d' % self.pk

    @classmethod
    def create(cls, user, idea, description, c_target, c_deadline, campaign_collected_sum=0):
        return cls(user=user, idea_ref=idea, title=idea.title, \
            idea=idea.idea, is_active=idea.is_active, description=description, \
            campaign_target_sum=c_target, meta_campaign_deadline=c_deadline, \
            campaign_collected_sum=campaign_collected_sum)
