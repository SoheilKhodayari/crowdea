# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Create your tests here.
class IndexTest(TestCase):

    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')
        
        test_user1.save()
        test_user2.save()

    def test_get_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_get_url_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_get_url_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, 'index.html')   

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse("authApp:getLogin"))

    def test_if_correct_user_is_logged_in(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("index"))
        self.assertEqual(str(response.context['user']), 'testuser1')