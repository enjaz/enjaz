# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def add_tags(apps, schema_editor):
    Tag = apps.get_model('arshidni', 'Tag')
    Tag.objects.create(name="إرشاد السنة التحضيرية الأولى")
    Tag.objects.create(name="إرشاد السنة التحضيرية الثانية")
    Tag.objects.create(name="إرشاد في التفوق الدراسي")
    Tag.objects.create(name="إرشاد في مجال الأبحاث")
    Tag.objects.create(name="إرشاد في الاختبارات العالمية")
    Tag.objects.create(name="إرشاد في التدريب الصيفي الإكلينيكي")
    Tag.objects.create(name="إرشاد في النشاط الطلابي")

def remove_tags(apps, schema_editor):
    Tag = apps.get_model('arshidni', 'Tag')
    Tag.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('arshidni', '0007_add_tag_report_feedback'),
    ]

    operations = [
       migrations.RunPython(
            add_tags,
            reverse_code=remove_tags),
    ]
