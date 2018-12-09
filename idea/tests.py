# # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.models import User
from crowdea.utility import reverse_with_query
from .views import getAddIdeaOnSuccessRedirectUrl
from .models import Idea, IdeaRank
from datetime import datetime
import json

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
        print ("URL: "+success_url)
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

    def test_view_own_ideas_success(self):
        # adding 2 ideas first:
        add_idea_endpoint = reverse("ideaApp:postAddIdea")
        idea1 = {'idea-title': 'testIdea1', 'idea-text': 'idea content 1', 'user': self.test_user,
                          'is_active': 'on'}
        self.client.post(add_idea_endpoint, idea1, follow=True)
        # now getting ideas:
        view_ideas_endpoint = reverse("ideaApp:getAllIdeas")
        response = self.client.get(view_ideas_endpoint)
        # checking http status:
        self.assertEqual(response.status_code, 200)
        # checking list size and contents. newest idea should come first:
        ideas_list = response.context['ideas']
        self.assertEqual(ideas_list.__len__(), 1)
        self.assertEqual(ideas_list[0].title, 'testIdea1')
        self.assertEqual(ideas_list[0].idea, 'idea content 1')
        self.assertEqual(ideas_list[0].user, self.test_user)
        self.assertEqual(ideas_list[0].is_active, False)

    def test_view_idea_success(self):
        # adding idea first:
        ideaInstance = Idea.objects.create(title="title", idea="idea",
                                           is_active=True, user=self.test_user)
        ideaInstance.save()
        # viewing idea now:
        view_idea_endpoint = reverse("ideaApp:getIdeaById", kwargs={'ideaId':ideaInstance.pk})
        response = self.client.get(view_idea_endpoint)
        # checking http status
        self.assertEqual(response.status_code, 200)
        idea_db = response.context['idea']
        self.assertEqual(idea_db.title, 'title')
        self.assertEqual(idea_db.idea, 'idea')
        self.assertEqual(idea_db.user, self.test_user)
        self.assertEqual(idea_db.is_active, True)

class IdeaRankTest(TestCase):
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
             'meta_last_updated_at': '11/10/2018',
             'rating' : 100},
            {'title': 'The perfect ecommerce website', 
             'is_active':True,
             'idea': 'Lorem ipsum dolor sit amet, consectetur' \
             'adipiscing elit. Nam blandit suscipit massa quis' \
             'pharetra. Aliquam aliquam pretium consectetur.' \
             'Sed lorem sapien, blandit sed suscipit id,' \
             'tristique sed tellus. Integer elementum pharetra ' \
             'odio eu vestibulum. Aenean et neque et mi aliquet ',
             'meta_created_at': '05/10/2018',
             'meta_last_updated_at': '25/11/2018',
             'rating' : 102},
             {'title': 'Football club management app', 
             'is_active':True,
             'idea': 'Lorem ipsum dolor sit amet, consectetur' \
             'adipiscing elit. Nam blandit suscipit massa quis' \
             'pharetra. Aliquam aliquam pretium consectetur.' \
             'Sed lorem sapien, blandit sed suscipit id,' \
             'tristique sed tellus. Integer elementum pharetra ' \
             'odio eu vestibulum. Aenean et neque et mi aliquet ',
             'meta_created_at': '20/07/2017',
             'meta_last_updated_at': '14/11/2018',
             'rating' : -100}]

        ranks_info = [
            {'idea_id': 0,
            'value': 1},
            {'idea_id': 1,
            'value': -1}]

        self.ideas = self._create_ideas(ideas_info, self.test_user1)
        self.ranks = self._create_ranks(ranks_info, self.ideas, self.test_user1)

    def _create_ideas(self, ideas_info, user):
        result = []
        for info in ideas_info:
            idea = Idea.objects.create(
                title=info['title'], 
                idea=info['idea'], 
                is_active=info['is_active'], 
                user=user,
                meta_created_at=datetime.strptime(info['meta_created_at'], '%d/%m/%Y'),
                meta_last_updated_at=datetime.strptime(info['meta_last_updated_at'], '%d/%m/%Y'),
                rating = info['rating'])
            idea.save()
            result.append(idea)
        return result

    def _create_ranks(self, ranks_info, ideas, user):
        result = []
        for info in ranks_info:
            rank = IdeaRank.objects.create(
                idea=ideas[info['idea_id']], 
                user=user,
                value = info['value'])
            rank.save()
            result.append(rank)
        return result

    # Get all idea ranks for user
    def test_get_all_idea_ranks_for_user_url_exists_at_desired_location(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')    
        response = self.client.get('/get-idea-ranks-for-user')
        self.assertEqual(response.status_code, 200)

    def test_get_all_idea_ranks_for_user_url_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("ideaApp:getAllIdeaRanksForUser"))
        self.assertEqual(response.status_code, 200)

    def test_get_all_idea_ranks_for_user_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("ideaApp:getAllIdeaRanksForUser"))
        self.assertRedirects(response, reverse("authApp:getLogin"))

    def test_get_all_idea_ranks_for_user_return_correct_data(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("ideaApp:getAllIdeaRanksForUser"))

        response = json.loads(response.content)
        self.assertEqual(len(response['ranks']), 2)

        expected = { self.ideas[0].id: 1, self.ideas[1].id: -1 }

        for item in response['ranks']:
            actual_rank = item['rank']
            expected_rank = expected[item['idea_id']]
            self.assertEqual(actual_rank, expected_rank)

    # Get all idea ranks for user
    def test_get_idea_rank_for_user_url_accessible_by_name(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("ideaApp:getIdeaRankForUser",
                                    kwargs={'idea_id':self.ideas[0].id}))
        self.assertEqual(response.status_code, 200)

    def test_get_idea_rank_for_user_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("ideaApp:getIdeaRankForUser",
                                    kwargs={'idea_id':self.ideas[0].id}))
        self.assertRedirects(response, reverse("authApp:getLogin"))
    
    def test_get_idea_rank_for_user_return_correct_data(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse("ideaApp:getIdeaRankForUser",
                                    kwargs={'idea_id':self.ideas[0].id}))

        response = json.loads(response.content)
        self.assertEqual(response['rank'], 1)

        response = self.client.get(reverse("ideaApp:getIdeaRankForUser",
                                    kwargs={'idea_id':self.ideas[2].id}))

        response = json.loads(response.content)
        self.assertEqual(response['rank'], 0)

    # Post rank
    def test_rank_idea_unranked_before_success(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse("ideaApp:postRankIdea"),
                                    {'idea_id': self.ideas[2].id, 'rank': 1})
        self.assertEqual(response.status_code, 200)
        
        response = json.loads(response.content)
        idea = Idea.objects.get(id=self.ideas[2].id)
        self.assertEqual(idea.rating, -99)
        self.assertEqual(response['rating'], -99)
        self.assertEqual(response['rank'], 1)

    def test_rank_idea_ranked_different_before_success(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        # Ranked positive before
        response = self.client.post(reverse("ideaApp:postRankIdea"),
                                    {'idea_id': self.ideas[0].id, 'rank': -1})
        self.assertEqual(response.status_code, 200)
        
        response = json.loads(response.content)
        idea = Idea.objects.get(id=self.ideas[0].id)
        idea_rank = IdeaRank.objects.filter(idea=idea, user=self.test_user1)[0]

        self.assertEqual(idea.rating, 98)
        self.assertEqual(idea_rank.value, -1)
        self.assertEqual(response['rating'], 98)
        self.assertEqual(response['rank'], -1)

        # Ranked negative before
        response = self.client.post(reverse("ideaApp:postRankIdea"),
                                    {'idea_id': self.ideas[1].id, 'rank': 1})
        self.assertEqual(response.status_code, 200)
        
        response = json.loads(response.content)
        idea = Idea.objects.get(id=self.ideas[1].id)
        idea_rank = IdeaRank.objects.filter(idea=idea, user=self.test_user1)[0]

        self.assertEqual(idea.rating, 104)
        self.assertEqual(idea_rank.value, 1)
        self.assertEqual(response['rating'], 104)
        self.assertEqual(response['rank'], 1)

    def test_rank_idea_ranked_identical_before_success(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')

        # Ranked positive before
        response = self.client.post(reverse("ideaApp:postRankIdea"),
                                    {'idea_id': self.ideas[0].id, 'rank': 1})
        self.assertEqual(response.status_code, 200)
        
        response = json.loads(response.content)
        idea = Idea.objects.get(id=self.ideas[0].id)
        idea_rank = IdeaRank.objects.filter(idea=idea, user=self.test_user1)[0]

        self.assertEqual(idea.rating, 99)
        self.assertEqual(idea_rank.value, 0)
        self.assertEqual(response['rating'], 99)
        self.assertEqual(response['rank'], 0)

        # Ranked negative before
        response = self.client.post(reverse("ideaApp:postRankIdea"),
                                    {'idea_id': self.ideas[1].id, 'rank': -1})
        self.assertEqual(response.status_code, 200)
        
        response = json.loads(response.content)
        idea = Idea.objects.get(id=self.ideas[1].id)
        idea_rank = IdeaRank.objects.filter(idea=idea, user=self.test_user1)[0]

        self.assertEqual(idea.rating, 103)
        self.assertEqual(idea_rank.value, 0)
        self.assertEqual(response['rating'], 103)
        self.assertEqual(response['rank'], 0)

    def test_rank_idea_missing_idea_id_failure(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse("ideaApp:postRankIdea"), {'rank': 1})
        self.assertEqual(response.status_code, 403)

    def test_rank_idea_idea_id_not_integer_failure(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse("ideaApp:postRankIdea"), 
                                    {'idea_id': "test", 'rank': 1})
        self.assertEqual(response.status_code, 403)

    def test_rank_idea_non_existent_idea_failure(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse("ideaApp:postRankIdea"), 
                                    {'idea_id': 10, 'rank': 1})
        self.assertEqual(response.status_code, 403)

    def test_rank_idea_missing_rank_failure(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse("ideaApp:postRankIdea"), {'idea_id': 1})
        self.assertEqual(response.status_code, 403)

    def test_rank_idea_rank_not_integer_failure(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse("ideaApp:postRankIdea"), 
                                    {'idea_id': 1, 'rank': "test"})
        self.assertEqual(response.status_code, 403)

    def test_rank_idea_invalid_rank_failure(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.post(reverse("ideaApp:postRankIdea"), 
                                    {'idea_id': 1, 'rank': 20})
        self.assertEqual(response.status_code, 403)
    