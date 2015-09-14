# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_college(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    female_presidency = Club.objects.get(english_name="Presidency (Riyadh/Female)",
                                         year=year_2015_2016)
    r_i_f = College.objects.create(city='R', section='NG', name='I',
                                   gender='F')
    Club.objects.create(name="كلية الصحة العامة والمعلوماتية الصحية",
                        english_name="College of Public Health and Health Informatics",
                        description="",
                        email="pending@ksau-hs.edu.sa",
                        parent=female_presidency,
                        gender="F",
                        year=year_2015_2016,
                        city="R",
                        college=r_i_f)

def remove_college(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    College = apps.get_model('clubs', 'College')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    College.objects.get(city='R', section='NG', name='I',
                        gender='F').delete()
    Club.objects.get(english_name="College of Public Health and Health Informatics",
                     city='R', gender='F', year=year_2015_2016)
    
class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0034_club_media_assessor'),
    ]

    operations = [
       migrations.RunPython(
            add_college,
            reverse_code=remove_college),
    ]
