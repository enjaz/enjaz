# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_can_review_niqati(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(english_name__in=["Presidency (Jeddah)",
                                          "Presidency (Al-Ahsa)",
                                          "Presidency (Riyadh/Female)",
                                          "Presidency (Riyadh/Male)"],
                        year=year_2015_2016).update(can_review_niqati=True)    


def remove_can_review_niqati(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(english_name__in=["Presidency (Jeddah)",
                                          "Presidency (Al-Ahsa)",
                                          "Presidency (Riyadh/Female)",
                                          "Presidency (Riyadh/Male)"],
                        year=year_2015_2016).update(can_review_niqati=False)

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0023_fix_can_review_niqati_description'),
    ]

    operations = [
       migrations.RunPython(
            add_can_review_niqati,
            reverse_code=remove_can_review_niqati),

    ]
