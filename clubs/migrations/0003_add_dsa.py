# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

DEANSHIP_ENGLISH_NAME = "Deanship of Student Affairs"

def add_dsa(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    Club.objects.create(name=u"عمادة شؤون الطلاب",
                        english_name=DEANSHIP_ENGLISH_NAME,
                        description="",
                        email="deanship_student_affairs@ksau-hs.edu.sa",
                        city="R",
                        visible=False,
                        can_review=True,
                        )

def delete_dsa(apps, schema_editor):
    dsa = Club.objects.get(english_name=DEANSHIP_ENGLISH_NAME)
    dsa.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0002_auto_20150606_1327'),
    ]

    operations = [
       migrations.RunPython(
            add_dsa,
            reverse_code=delete_dsa),
    ]
