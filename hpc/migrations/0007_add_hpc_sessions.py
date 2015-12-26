# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def add_sessions(apps, schema_editor):
    Session = apps.get_model('hpc', 'Session')
    Session.objects.create(name="البرنامج العام وبرنامج الأبحاث",
                           time_slot=1,
                           vma_id=412)
    Session.objects.create(name="برنامج كلية التمريض",
                           time_slot=2,
                           vma_id=413,
                           gender='F')
    Session.objects.create(name="برنامج كلية طب الأسنان - طالبات",
                           time_slot=2,
                           vma_id=414,
                           gender='F')
    Session.objects.create(name="برنامج كلية طب الأسنان - طلاب",
                           time_slot=2,
                           vma_id=415,
                           gender='M')
    Session.objects.create(name="‫‪Workshop: Resrearch Question & Literature Review",
                           time_slot=2,
                           vma_id=0,
                           gender='M')
    Session.objects.create(name="‫‪Workshop: Study Design",
                           time_slot=2,
                           vma_id=0,
                           gender='M')
    Session.objects.create(name="‫‪‫‪Workshop: Scientific Writing",
                           time_slot=2,
                           vma_id=0,
                           gender='M')
    Session.objects.create(name="‫‪Workshop: Data Analysis & Manipulation",
                           time_slot=2,
                           vma_id=0,
                           gender='M')
    Session.objects.create(name="Workshop: Resrearch Question & Literature Review",
                           time_slot=2,
                           vma_id=0,
                           gender='F')
    Session.objects.create(name="‫‪Workshop: Study Design",
                           time_slot=2,
                           vma_id=0,
                           gender='F')
    Session.objects.create(name="‫‪‫‪Workshop: Scientific Writing",
                           time_slot=2,
                           vma_id=0,
                           gender='F')
    Session.objects.create(name="‫‪Workshop: Data Analysis & Manipulation",
                           time_slot=2,
                           vma_id=0,
                           gender='F')
    Session.objects.create(name="ورشة عمل: تعزيز الثقة بالنفس",
                           time_slot=3,
                           vma_id=0)
    Session.objects.create(name="‫‪ورشة عمل: كيف تتخطى المقابلة الشخصية؟",
                           time_slot=3,
                           vma_id=0)
    Session.objects.create(name="‫‪ورشة عمل: التعامل مع الضغوط الدراسية",
                           time_slot=3,
                           vma_id=0)
    Session.objects.create(name="برنامج كلية الصيدلة",
                           time_slot=3,
                           vma_id=416)
    Session.objects.create(name="برنامج كلية العلوم الطبية التطبيقية - طلاب",
                           time_slot=3,
                           vma_id=417,
                           gender='M')
    Session.objects.create(name="برنامج كلية العلوم الطبية التطبيقية - طالبات",
                           time_slot=3,
                           vma_id=418,
                           gender='F')
    Session.objects.create(name="برنامج كلية الطب",
                           time_slot=3,
                           vma_id=419)
    Session.objects.create(name="ورشة عمل: تجربة اختبار SMLE",
                           time_slot=None,
                           vma_id=0)


def remove_sessions(apps, schema_editor):
    Session = apps.get_model('hpc', 'Session')
    Session.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('hpc', '0006_registration'),
    ]

    operations = [
       migrations.RunPython(
            add_sessions,
            reverse_code=remove_sessions),
    ]
