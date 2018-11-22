# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from crowdea.utility import reverse_with_query

# Create your tests here.
class LoginTest(TestCase):

    def setUp(self):
        # Create a user
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

        self.login_fail_msg = '?error=Wrong+credentials+try+again'

    # GET
    def test_get_url_exists_at_desired_location(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_get_url_accessible_by_name(self):
        response = self.client.get(reverse("authApp:getLogin"))
        self.assertEqual(response.status_code, 200)

    def test_get_uses_correct_template(self):
        response = self.client.get(reverse("authApp:getLogin"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'authentication/login.html')

    # POST
    def test_login_succesfull_with_corrent_user(self):
        response = self.client.post(reverse("authApp:postLogin"), 
            {'username': 'testuser1', 'password': '1X<ISRUkw+tuK'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)

    def test_redirects_to_index_on_success(self):
        response = self.client.post(reverse("authApp:postLogin"), 
            {'username': 'testuser1', 'password': '1X<ISRUkw+tuK'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("index"))

    def test_login_fails_with_invalid_user(self):
        response = self.client.post(reverse("authApp:postLogin"), 
            {'username': 'test', 'password': 'test'}, follow=True)
        self.assertRedirects(response, '%s%s' % (reverse("authApp:getLogin"),self.login_fail_msg))

    def test_login_fails_with_missing_username(self):
        response = self.client.post(reverse("authApp:postLogin"), {'password': 'test'}, follow=True)
        self.assertRedirects(response, '%s%s' % (reverse("authApp:getLogin"),self.login_fail_msg))

    def test_login_fails_with_missing_password(self):
        response = self.client.post(reverse("authApp:postLogin"), {'username': 'test'}, follow=True)
        self.assertRedirects(response, '%s%s' % (reverse("authApp:getLogin"),self.login_fail_msg))

    def test_login_fails_with_missing_credentials(self):
        response = self.client.post(reverse("authApp:postLogin"), {}, follow=True)
        self.assertRedirects(response, '%s%s' % (reverse("authApp:getLogin"),self.login_fail_msg))


class LogoutTest(TestCase):

    def test_url_exists_at_desired_location(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("authApp:getLogout"))
        self.assertEqual(response.status_code, 302)

    def test_redirect_to_login(self):
        response = self.client.get(reverse("authApp:getLogout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("authApp:getLogin"))

    def test_logout_succesfull(self):
        response = self.client.get(reverse("authApp:getLogout"))
        self.assertNotIn('_auth_user_id', self.client.session)


class RegisterTest(TestCase):

    def setUp(self):
        # Create a user to check for failure scenario
        test_user = User.objects.create_user(username='test@test.com', password='1X<ISRUkw+tuK')
        test_user.save()

        # register post endpoint shared among all test cases
        self.register_endpoint = reverse("authApp:postRegister")

    def test_register_success(self):
        # actual
        kwargs = {
                  'username': 'test@gmail.com',
                  'password': 'test1Pa$$worD',
                  'firstname':'testfname',
                  'lastname': 'testlname',
        }
        response = self.client.post(self.register_endpoint, kwargs ,follow=True)

        # expected
        success_query_kwargs = {"Reg-Msg":"Successful"}
        success_url = reverse_with_query("index", success_query_kwargs)

        # assert and compare
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, success_url)

    def test_register_fails_on_existing_username(self):
        kwargs = {
                  'username': 'test@test.com',
                  'password': 'test1Pa$$worD',
                  'firstname':'testfname',
                  'lastname': 'testlname',
        }
        response = self.client.post(self.register_endpoint, kwargs ,follow=True)

        # expected:
        error_query_kwargs = {"Reg-Msg":"Error-Username-Exists"}
        success_url = reverse_with_query("authApp:getRegister",error_query_kwargs)

        # assert the application don't breaks
        self.assertEqual(response.status_code, 200)

        # assert the redirect response
        self.assertRedirects(response, success_url)

    def test_register_fails_on_empty_fields(self):

        kwargs = {
                  'username': 'test@test.com',
                  'password': '',
                  'firstname':'',
                  'lastname': 'testlname',
        }
        response = self.client.post(self.register_endpoint, kwargs ,follow=True)

        # expected:
        error_query_kwargs = {"Reg-Msg":"Incomplete-Data"}
        success_url = reverse_with_query("authApp:getRegister",error_query_kwargs)

        # assert the application don't breaks
        self.assertEqual(response.status_code, 200)

        # assert the redirect response
        self.assertRedirects(response, success_url)

