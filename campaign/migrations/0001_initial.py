# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import campaign.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('idea', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('idea', models.TextField(blank=True, max_length=500, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=1000)),
                ('meta_created_at', models.DateTimeField(auto_now_add=True)),
                ('campaign_target_sum', models.IntegerField()),
                ('campaign_collected_sum', models.IntegerField(default=0)),
                ('meta_campaign_deadline', models.DateTimeField(validators=[campaign.utils.validate_campaign_target])),
                ('idea_ref', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='idea.Idea')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
