# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    presidency = Club.objects.get(english_name="Presidency", year=year_2015_2016)
    Club.objects.create(english_name="Research Committee of the HPC",
                        name="لجنة أبحاث مؤتمر التخصصات الصحية",
                        gender="",
                        parent=presidency,
                        email="hpp@ksau-hs.edu.sa",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)
    Club.objects.create(english_name="Organizing Committee of the HPC",
                        name="لجنة تنظيم مؤتمر التخصصات الصحية",
                        gender="",
                        parent=presidency,
                        email="hpp@ksau-hs.edu.sa",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)

def remove_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(english_name__in=["ٌOrganizing Committee of the HPC",
                                          "ٌResearch Committee of the HPC"],
                        year=year_2015_2016).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0002_abstract_level'),
        ('clubs', '0038_club_can_submit_activities'),
    ]

    operations = [
       migrations.RunPython(
            add_clubs,
            reverse_code=remove_clubs),
    ]
