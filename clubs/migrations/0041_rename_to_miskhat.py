# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def rename(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(name="نادي البحث والابتكار والتقنية",
                        year=year_2015_2016).update(name="مشكاة")
    Club.objects.filter(english_name="Research, Innovation and Technology Club",
                        year=year_2015_2016).update(english_name="Mishkat")

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0040_club_can_skip_followup_reports'),
    ]

    operations = [
        migrations.RunPython(rename)
    ]
