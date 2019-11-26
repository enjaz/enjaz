# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0012_auto_20191018_1553'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sorting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('study_design', models.IntegerField(verbose_name='Study Design', choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])),
                ('data_recency', models.IntegerField(verbose_name='Data Recency', choices=[(0, 0), (1, 1), (2, 2), (3, 3)])),
                ('status', models.IntegerField(verbose_name='Presentation Status', choices=[(1, 1), (2, 2)])),
                ('pres_author_affiliation', models.IntegerField(verbose_name='Presenter Author Affiliation', choices=[(0, 0), (2, 2), (3, 3)])),
                ('research_value', models.IntegerField(verbose_name='Research Value', choices=[(1, 1), (3, 3), (5, 5)])),
                ('pub_status', models.IntegerField(verbose_name='Publication Status', choices=[(0, 0), (1, 1), (2, 2)])),
                ('sorting_score', models.IntegerField(verbose_name='\u0627\u0644\u0642\u064a\u0645\u0629')),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('abstract', models.ForeignKey(to='events.Abstract')),
                ('sorter', models.ForeignKey(related_name='event_abstract_sortings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
