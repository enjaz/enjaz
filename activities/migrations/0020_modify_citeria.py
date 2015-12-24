# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="التعاون مع الرئاسة",
                             code_name="presidency",
                             instructions="",
                             category='P')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="رفع مبكر",
                             code_name="early_submission",
                             instructions="",
                             category='P')
    Criterion.objects.create(year=year_2015_2016,
                             ar_name="تأجيل",
                             code_name="postponed",
                             instructions="",
                             category='P')
    Criterion.objects.get(code_name='time', category='P').delete()

def remove_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Criterion.objects.filter(code_name__in=["presidency",
                                            "early_submission", "postponed"]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0019_remove_alahsa_criteria'),
    ]

    operations = [
       migrations.RunPython(
            add_criteria,
            reverse_code=remove_criteria),
    ]
