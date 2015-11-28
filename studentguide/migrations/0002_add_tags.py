# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_tags(apps, schema_editor):
    Tag = apps.get_model('studentguide', 'Tag')
    Tag.objects.create(name="إرشاد في اللغة الإنجليزية", code_name="english")
    Tag.objects.create(name="إرشاد في المواد العلمية للسنة الأولى", code_name="first_year")
    Tag.objects.create(name="إرشاد في المواد العلمية للسنة الثانية", code_name="second_year")
    Tag.objects.create(name="إرشاد في النشاط الطلابي", code_name="extracurricular")
    Tag.objects.create(name="إرشاد في البحث العلمي", code_name="research")
    Tag.objects.create(name="إرشاد في الاختبارات العالمية", code_name="international_exams")
    Tag.objects.create(name="إرشاد في التدريب الصيفي", code_name="elective_training")

def remove_tags(apps, schema_editor):
    Tag = apps.get_model('studentguide', 'Tag')
    Tag.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('studentguide', '0001_initial'),
    ]

    operations = [
       migrations.RunPython(
            add_tags,
            reverse_code=remove_tags),
    ]
