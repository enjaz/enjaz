# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def remove_alahsa(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Criterion.objects.filter(code_name__in=['advertisement',
                                            'news_punctuality',
                                            'news_quality',
                                            'interactivity']).update(city='RJ')

def add_alahsa(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Criterion.objects.filter(code_name__in=['advertisement',
                                            'news_punctuality',
                                            'news_quality',
                                            'interactivity']).update(city='RAJ')

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0018_criterion_city'),
    ]

    operations = [
       migrations.RunPython(
            remove_alahsa,
            reverse_code=add_alahsa),
    ]
