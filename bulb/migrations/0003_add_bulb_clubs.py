# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    arshidny_male = Club.objects.get(english_name__in=["Arshidny", "Arshidni"],
                                     gender='F',
                                     year=year_2015_2016)
    arshidny_female = Club.objects.get(english_name__in=["Arshidny", "Arshidni"],
                                       gender='M',
                                       year=year_2015_2016)
    Club.objects.create(english_name="Bulb",
                        name="سراج",
                        gender="M",
                        year=year_2015_2016,
                        parent=arshidny_male,
                        email="arshidny@ksau-hs.edu.sa",
                        city="الرياض",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)

    Club.objects.create(english_name="Bulb",
                        name="سراج",
                        gender="F",
                        year=year_2015_2016,
                        parent=arshidny_female,
                        email="arshidny@ksau-hs.edu.sa",
                        city="الرياض",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)

def remove_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(english_name="Bulb",
                        year=year_2015_2016).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0002_add_categories'),
        ('clubs', '0038_club_can_submit_activities'),
    ]

    operations = [
       migrations.RunPython(
            add_clubs,
            reverse_code=remove_clubs),
    ]
