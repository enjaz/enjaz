# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_sessions(apps, schema_editor):
    Session = apps.get_model('hpc', 'Session')
    Session.objects.filter(name="البرنامج العام وبرنامج الأبحاث").update(time_slot=None, code_name='main')
    Session.objects.filter(name="ورشة عمل: تجربة اختبار SMLE").update(code_name='smle')
    Session.objects.create(name="محاضرة ECG",
                           time_slot=4,
                           vma_id=0)
    Session.objects.create(name="محاضرة Antibiotics",
                           time_slot=4,
                           vma_id=0)
    Session.objects.create(name="جلسة المجموعات العلاجية",
                           time_slot=None,
                           code_name='therapy',
                           vma_id=0,
                           gender='F')

class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0009_add_missing_fields'),
    ]

    operations = [
       migrations.RunPython(
            add_sessions),
    ]
