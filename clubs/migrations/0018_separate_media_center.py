# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def separate_media_center(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015, end_date__year=2016)
    presidency2015_2016 = Club.objects.get(english_name="Presidency", year=year2015_2016)
    mc2015_2016 = Club.objects.create(
        name="المركز الإعلامي",
        english_name="Media Center",
        parent=presidency2015_2016, 
        description="",
        year=year2015_2016,
        email="sc-media@ksau-hs.edu.sa",
        visible=False,
        can_review=False,
        city="R",
        )

def unify_media_center(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year2015_2016 = StudentClubYear.objects.get(start_date__year=2015, end_date__year=2016)
    Club.objects.get(english_name="Media Center", year=year2015_2016).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0017_club_can_delete'),
    ]

    operations = [
        migrations.RunPython(
            separate_media_center,
            reverse_code=unify_media_center),
    ]
