# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_media_cetners(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    presidency2015_2016 = Club.objects.get(english_name="Presidency", year=year_2015_2016)
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency2015_2016, 
        description="",
        year=year_2015_2016,
        email="sc-mediaj@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,
        city="J")
    Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency2015_2016, 
        description="",
        year=year_2015_2016,
        email="sc-mediaah@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        can_assess=True,        
        city="A")

def remove_media_cetners(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(english_name="Media Center", year=year_2015_2016, city__in=['J', 'A']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0025_assessment'),
    ]

    operations = [
        migrations.RunPython(
            add_media_cetners,
            reverse_code=remove_media_cetners),
    ]
