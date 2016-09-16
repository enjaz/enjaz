# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    arshidny_male = Club.objects.get(english_name__in=["Arshidny", "Arshidni"],
                                     gender='F', city="R",
                                     year=year_2016_2017)
    arshidny_female = Club.objects.get(english_name__in=["Arshidny", "Arshidni"],
                                       gender='M', city="R",
                                       year=year_2016_2017)
    arshidny_jeddah = Club.objects.get(english_name__in=["Arshidny", "Arshidni"],
                                       city="J", year=year_2016_2017)
    arshidny_alahsa = Club.objects.get(english_name__in=["Arshidny", "Arshidni"],
                                       city="A", year=year_2016_2017)
    Club.objects.create(english_name="Student Guide",
                        name="المرشد الطلابي",
                        gender="M",
                        year=year_2016_2017,
                        parent=arshidny_male,
                        email="arshidny@ksau-hs.edu.sa",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)
    Club.objects.create(english_name="Student Guide",
                        name="المرشد الطلابي",
                        gender="F",
                        year=year_2016_2017,
                        parent=arshidny_female,
                        email="arshidny@ksau-hs.edu.sa",
                        city="R",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)
    Club.objects.create(english_name="Student Guide",
                        name="المرشد الطلابي",
                        gender="",
                        year=year_2016_2017,
                        parent=arshidny_jeddah,
                        email="arshidny@ksau-hs.edu.sa",
                        city="J",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)
    Club.objects.create(english_name="Student Guide",
                        name="المرشد الطلابي",
                        gender="",
                        year=year_2016_2017,
                        parent=arshidny_alahsa,
                        email="arshidny@ksau-hs.edu.sa",
                        city="J",
                        visible=False,
                        can_view_assessments=False,
                        is_assessed=False,
                        can_submit_activities=False)

def remove_clubs(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    Club.objects.filter(english_name="Student Guide",
                        year=year_2016_2017).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('studentguide', '0011_non_required_academic'),
        ('clubs', '0046_add_jeddah_ams_deanship'),
    ]

    operations = [
       migrations.RunPython(
            add_clubs,
            reverse_code=remove_clubs),
    ]
