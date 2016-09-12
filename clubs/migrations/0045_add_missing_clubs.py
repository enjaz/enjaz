# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_college(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    jeddah_presidency = Club.objects.get(english_name="Presidency",
                                         year=year_2016_2017, city="J")
    male_presidency = Club.objects.get(english_name="Presidency",
                                       year=year_2016_2017,
                                       city="R",gender="M")
    j_a_f = College.objects.create(city='J', section='J', name='A',
                                gender='F')
    j_a_m = College.objects.create(city='J', section='J', name='A',
                                   gender='M')
    Club.objects.create(name="كلية العلوم الطبية التطبيقية",
                        english_name="College of Applied Medical Sciences",
                        description="",
                        email="sc-cams@ksau-hs.edu.sa",
                        parent=jeddah_presidency,
                        gender="",
                        year=year_2016_2017,
                        city="J",
                        college=j_a_f)

def remove_college(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    College.objects.get(city='J', section='J', name='A', gender='F').delete()
    College.objects.get(city='J', section='J', name='A', gender='M').delete()
    Club.objects.get(english_name="College of Applied Medical Sciences",
                     city='J', year=year_2016_2017).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0044_add_jeddah_ahsa_deanships'),
    ]

    operations = [
       migrations.RunPython(
            add_college,
            reverse_code=remove_college),
    ]
