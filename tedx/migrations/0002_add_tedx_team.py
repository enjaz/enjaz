# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_tedx_team(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Event = apps.get_model('events', 'Event')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)

    tedx_team = Team.objects.create(name="فريق التسجيل لتدكس 2017",
                                    code_name="tedx_2017_registration",
                                    year=year_2016_2017,
                                    city="R", gender="")

def remove_tedx_team(apps, schema_editor):
    Team = apps.get_model('clubs', 'Team')
    Team.objects.filter(code_name="tedx_2017_registration").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('tedx', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_tedx_team,
            reverse_code=remove_tedx_team),
    ]
