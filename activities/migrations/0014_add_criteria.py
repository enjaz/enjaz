# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="النوع",
                             code_name="type",
                             instructions="",
                             category='p')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="أجزاء النشاط وسلاسل الأنشطة",
                             code_name="episodes",
                             instructions="",
                             category='p')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="الفكرة",
                             code_name="student_idea",
                             instructions="",
                             category='p')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="الفكرة",
                             code_name="creative_idea",
                             instructions="",
                             category='p')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="الوقت",
                             code_name="time",
                             instructions="",
                             category='p')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="الحضور",
                             code_name="attendees",
                             instructions="",
                             category='p')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="تقييم الطلاب",
                             code_name="student_evaluation",
                             instructions="",
                             category='p')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="المركز الإعلامي",
                             code_name="media_center",
                             instructions="",
                             category='m')

def remove_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Criterion.objects.filter(year=year_2015_2016).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0013_assessment'),
    ]

    operations = [
       migrations.RunPython(
            add_criteria,
            reverse_code=remove_criteria),
    ]
