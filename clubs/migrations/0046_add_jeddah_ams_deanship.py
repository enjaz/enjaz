# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_deanship(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    jeddah_presidency = Club.objects.get(english_name="Presidency", city="J",
                                         year=year_2016_2017)

    j_a_c = Club.objects.get(english_name="College of Applied Medical Sciences",
                             city="J", year=year_2016_2017)

    j_a_d = Club.objects.create(name="عمادة كلية العلوم الطبية التطبيقية",
                                english_name="Deanship of the College of Applied Medical Sciences",
                                description="",
                                email="pending@ksau-hs.edu.sa",
                                parent=jeddah_presidency,
                                city="J",
                                year=year_2016_2017,
                                visible=False,
                                can_review=True,
                                can_delete=False,
                                can_edit=False)
    j_a_c.parent = j_a_d
    j_a_c.save()

def remove_deanship(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    jeddah_presidency = Club.objects.get(english_name="Presidency", city="J",
                                         year=year_2016_2017)
    Club.objects.get(english_name="Deanship of the College of Applied Medical Sciences",
                     city="J", year=year_2016_2017).delete()
    j_a_c = Club.objects.get(english_name="College of Applied Medical Sciences",
                             city="J", year=year_2016_2017)
    j_a_c.parent = jeddah_presidency
    j_a_c.save()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0045_add_missing_clubs'),
    ]

    operations = [
       migrations.RunPython(add_deanship,
                            reverse_code=remove_deanship)
    ]
