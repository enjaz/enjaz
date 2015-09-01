# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    # Remove the single media criterion, to replace it with more
    # specific criteria.
    Criterion.objects.get(year=year_2015_2016, code_name="media_center", category='M').delete()
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="التقرير",
                             code_name="report",
                             instructions="",
                             category='M')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="الإعلان",
                             code_name="advertisement",
                             instructions="",
                             category='M')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="سرعة الخبر",
                             code_name="news_punctuality",
                             instructions="",
                             category='M')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="جودة الخبر",
                             code_name="news_quality",
                             instructions="",
                             category='M')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="جودة الصور والإعلان",
                             code_name="image_quality",
                             instructions="",
                             category='M')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="التفاعل",
                             code_name="interactivity",
                             instructions="",
                             category='M')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="المخالفات",
                             code_name="violations",
                             instructions="",
                             category='M')


def remove_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Criterion.objects.filter(year=year_2015_2016, category='M').delete()
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="المركز الإعلامي",
                             code_name="media_center",
                             instructions="",
                             category='M')

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0016_is_reviewed'),
    ]

    operations = [
       migrations.RunPython(
            add_criteria,
            reverse_code=remove_criteria),
    ]
