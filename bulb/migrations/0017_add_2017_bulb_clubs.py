# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    presidency = Club.objects.get(english_name="Presidency",
                                  year=year_2016_2017, gender="",
                                  city="R")

    Club.objects.create(english_name="Bulb",
                        name="سراج",
                        gender="M",
                        year=year_2016_2017,
                        parent=presidency,
                        email="bulb@enjazportal.com",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)

    Club.objects.create(english_name="Bulb",
                        name="سراج",
                        gender="F",
                        year=year_2016_2017,
                        parent=presidency,
                        email="bulb@enjazportal.com",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)

def remove_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    Club.objects.filter(english_name="Bulb",
                        year=year_2016_2017).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('bulb', '0016_add_recruitment'),
        ('clubs', '0043_add_2016_clubs'),
    ]

    operations = [
       migrations.RunPython(
            add_clubs,
            reverse_code=remove_clubs),
    ]
