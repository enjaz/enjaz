# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def add_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year= 2016,
                                                end_date__year=2017)
    Criterion.objects.create(year= year_2016_2017,
                            ar_name="مكان النشاط",
                            code_name="place",
                            instructions="",
                            category='P')
    Criterion.objects.create(year= year_2016_2017,
                            ar_name="التعاون",
                            code_name="cooperation",
                            instructions="",
                            category='P')
    Criterion.objects.create(year= year_2016_2017,
                            ar_name="توقيت النشاط بعدد الأيام",
                            code_name="activity_days",
                            instructions="",
                            category='P')
    Criterion.objects.create(year= year_2016_2017,
                            ar_name="توقيت النشاط بعدد الساعات",
                            code_name="activity_hours",
                            instructions="",
                            category='P')
    Criterion.objects.create(year= year_2016_2017,
                                ar_name="عدد الحضور",
                                code_name="attendees",
                                instructions="",
                                category='P')
    Criterion.objects.create(year= year_2016_2017,
                                ar_name="فكرة غير تقليدية",
                                code_name="new_idea",
                                instructions="",
                                category='P')
    Criterion.objects.create(year= year_2016_2017,
                                    ar_name="تفرع الفكرة",
                                    code_name="branched_idea",
                                    instructions="",
                                    category='P')
    Criterion.objects.create(year= year_2016_2017,
                                ar_name="فكرة مقترحة من طالب/ة",
                                code_name="student_idea",
                                instructions="",
                                category='P')

    Criterion.objects.create(year= year_2016_2017,
                            ar_name="طرح الفكرة بطريقة غير تقليدية",
                            code_name="creative_idea",
                            instructions="",
                            category='P')
    Criterion.objects.create(year= year_2016_2017,
                                              ar_name="استعمال وسائل مصاحبة",
                                              code_name="use_resources",
                                              instructions="",
                                              category='P')
    Criterion.objects.create(year= year_2016_2017,
                            ar_name="الشكل العام",
                            code_name="apperance",
                            instructions="",
                            category='P')
    Criterion.objects.create(year= year_2016_2017,
                                              ar_name="تنظيم الحضور",
                                              code_name="attendees_orgnisation",
                                              instructions="",
                                              category='P')
    Criterion.objects.create(year= year_2016_2017,
                                                  ar_name="رضا الحضور",
                                                  code_name="attendees_satisfaction",
                                                  instructions="",
                                                  category='P')
    Criterion.objects.create(year= year_2016_2017,
                                                  ar_name="إدارة النشاط",
                                                  code_name="orgnisation",
                                                  instructions="",
                                                  category='P')

def remove_criteria(apps, schema_editor):
    Criterion = apps.get_model('activities', 'Criterion')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2016_2017 = StudentClubYear.objects.get(start_date__year=2016,
                                                 end_date__year=2017)
    Criterion.objects.filter(year=year_2016_2017).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0026_invitation_twitter_account'),
        ('core', '0009_tweet_failed_trials')
    ]

    operations = [
       migrations.RunPython(
            add_criteria,
            reverse_code=remove_criteria),
    ]
