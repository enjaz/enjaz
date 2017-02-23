# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    # Most previous criteria should be limited to Riyadh (others are
    # still shared)
    Criterion.objects.filter(year=year_2016_2017).exclude(code_name__in=['creative_idea',
                                                                         'student_idea'])\
                                                 .update(city="الرياض")

    Criterion.objects.create(year=year_2016_2017,
                             ar_name="النوع",
                             code_name="type",
                             instructions="",
                             city="JA",
                             category='P')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="أجزاء النشاط وسلاسل الأنشطة",
                             code_name="episodes",
                             instructions="",
                             city="JA",
                             category='P')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="التعاون مع الرئاسة",
                             code_name="presidency",
                             instructions="",
                             city="JA",
                             category='P')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="رفع مبكر",
                             code_name="early_submission",
                             instructions="",
                             city="JA",
                             category='P')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="تأجيل",
                             code_name="postponed",
                             instructions="",
                             city="JA",
                             category='P')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="تقييم الطلاب",
                             code_name="student_evaluation",
                             instructions="",
                             city="JA",
                             category='P')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="التقرير",
                             code_name="report",
                             instructions="",
                             city="JA",
                             category='M')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="الإعلان",
                             code_name="advertisement",
                             instructions="",
                             city="JA",
                             category='M')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="سرعة الخبر",
                             code_name="news_punctuality",
                             instructions="",
                             city="JA",
                             category='M')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="جودة الخبر",
                             code_name="news_quality",
                             instructions="",
                             city="JA",
                             category='M')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="جودة الصور والإعلان",
                             code_name="image_quality",
                             instructions="",
                             city="JA",
                             category='M')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="التفاعل",
                             code_name="interactivity",
                             instructions="",
                             city="JA",
                             category='M')
    Criterion.objects.create(year=year_2016_2017,
                             ar_name="المخالفات",
                             code_name="violations",
                             instructions="",
                             city="JA",
                             category='M')

def remove_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    Criterion.objects.filter(year=year_2016_2017, city="JA").delete()
    Criterion.objects.filter(year=year_2016_2017, category="M").delete()
    # Generalize all previous criteria
    Criterion.objects.filter(year=year_2016_2017).update(city="RAJ")

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0040_enhance_cooperator_points'),
    ]

    operations = [
       migrations.RunPython(
            add_criteria,
            reverse_code=remove_criteria),
    ]
