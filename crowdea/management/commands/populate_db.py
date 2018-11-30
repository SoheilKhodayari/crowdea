from django.core.management.base import BaseCommand
from idea.models import Idea
from campaign.models import Campaign
from datetime import datetime
from django.contrib.auth.models import User

users_info = [
    {'username': 'thor@valhala.sky', 'password': 'thor1234'},
    {'username': 'loki@valhala.sky', 'password': 'loki1234'},
    {'username': 'odin@valhala.sky', 'password': 'odin1234'},
    {'username': 'nemo@pacific.oc', 'password': 'nemo1234'},
    {'username': 'dori@pacific.oc', 'password': 'dori1234'}]
users = [] # Filled by script

ideas_info = [
    {'title': 'New app for food delivery', 
     'is_active':True, 'user':0,
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
     'is_active':True, 'user':0,
     'idea': 'Lorem ipsum dolor sit amet, consectetur' \
     'adipiscing elit. Nam blandit suscipit massa quis' \
     'pharetra. Aliquam aliquam pretium consectetur.' \
     'Sed lorem sapien, blandit sed suscipit id,' \
     'tristique sed tellus. Integer elementum pharetra ' \
     'odio eu vestibulum. Aenean et neque et mi aliquet ',
     'meta_created_at': '05/10/2018',
     'meta_last_updated_at': '25/11/2018'},
    {'title': 'Community helping platform',
     'is_active':True, 'user':1,
     'idea': 'Lorem ipsum dolor sit amet, consectetur' \
     'adipiscing elit. Nam blandit suscipit massa quis' \
     'pharetra. Aliquam aliquam pretium consectetur.' \
     'Sed lorem sapien, blandit sed suscipit id,' \
     'tristique sed tellus. Integer elementum pharetra ' \
     'odio eu vestibulum. Aenean et neque et mi aliquet ',
     'meta_created_at': '17/09/2018',
     'meta_last_updated_at': '18/09/2018'},
    {'title': 'Personal assistant', 
     'is_active':True, 'user':2,
     'idea': 'Lorem ipsum dolor sit amet, consectetur' \
     'adipiscing elit. Nam blandit suscipit massa quis' \
     'pharetra. Aliquam aliquam pretium consectetur.' \
     'Sed lorem sapien, blandit sed suscipit id,' \
     'tristique sed tellus. Integer elementum pharetra ' \
     'odio eu vestibulum. Aenean et neque et mi aliquet ',
     'meta_created_at': '20/02/2017',
     'meta_last_updated_at': '14/04/2017'},
    {'title': 'Football club management app', 
     'is_active':True, 'user':2,
     'idea': 'Lorem ipsum dolor sit amet, consectetur' \
     'adipiscing elit. Nam blandit suscipit massa quis' \
     'pharetra. Aliquam aliquam pretium consectetur.' \
     'Sed lorem sapien, blandit sed suscipit id,' \
     'tristique sed tellus. Integer elementum pharetra ' \
     'odio eu vestibulum. Aenean et neque et mi aliquet ',
     'meta_created_at': '20/07/2017',
     'meta_last_updated_at': '14/11/2018'}]

ideas = [] # Filled by the script

campaigns_info = [
    {'user': 0, 'idea': 1,
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
    {'user': 1, 'idea': 2,
     'description': 'Integer pellentesque ornare' \
     ' diam, id blandit neque dictum sit amet. Etiam' \
     ' ultrices est ac lorem commodo gravida. Phasellus' \
     ' scelerisque tortor tincidunt lacus ornare, a finibus' \
     ' turpis tristique. Donec tortor nisl, maximus ut'\
     'volutpat sit amet, sodales ut odio. ',
     'campaign_target_sum': 5000,
     'campaign_collected_sum': 4700,
     'meta_created_at': '23/10/2018',
     'meta_campaign_deadline': '31/12/2019'},
    {'user': 2, 'idea': 4,
     'description': 'Integer pellentesque ornare' \
     ' diam, id blandit neque dictum sit amet. Etiam' \
     ' ultrices est ac lorem commodo gravida. Phasellus' \
     ' scelerisque tortor tincidunt lacus ornare, a finibus' \
     ' turpis tristique. Donec tortor nisl, maximus ut'\
     'volutpat sit amet, sodales ut odio. ',
     'campaign_target_sum': 12000,
     'campaign_collected_sum': 5000,
     'meta_created_at': '01/12/2017',
     'meta_campaign_deadline': '05/06/2019'}]

class Command(BaseCommand):
    args = ''
    help = 'Populate the database with dummy data to' \
           'be used for testing'
    
    def handle(self, *args, **options):
        self._create_users()
        self._create_ideas()
        self._create_campaigns()
    
    def _create_users(self):
        for info in users_info:
            user = User.objects.create_user(
                username=info['username'], 
                password=info['password'])
            user.save()
            users.append(user)

    def _create_ideas(self):
        for info in ideas_info:
            idea = Idea.objects.create(
                title=info['title'], 
                idea=info['idea'], 
                is_active=info['is_active'], 
                user=users[info['user']],
                meta_created_at=datetime.strptime(info['meta_created_at'], '%d/%m/%Y'),
                meta_last_updated_at=datetime.strptime(info['meta_last_updated_at'], '%d/%m/%Y'))
            idea.save()
            ideas.append(idea)

    def _create_campaigns(self):
        for info in campaigns_info:
            campaign = Campaign.create(
                user=users[info['user']],
                idea=ideas[info['idea']],
                description=info['description'],
                c_target=info['campaign_target_sum'],
                collected=info['campaign_collected_sum'],
                c_deadline=datetime.strptime(info['meta_campaign_deadline'], '%d/%m/%Y'))
            campaign.save()
