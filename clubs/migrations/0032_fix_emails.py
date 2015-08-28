# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def fix_emails(apps, schema_editor):
    Club = apps.get_model('clubs', 'Club')
    StudentClubYear = apps.get_model('core', 'StudentClubYear')
    year_2015_2016 = StudentClubYear.objects.get(start_date__year=2015,
                                                 end_date__year=2016)
    Club.objects.filter(year=year_2015_2016, city='R', gender='F',
                        email='sc-com@ksau-hs.edu.sa').update(email='sc-comf@ksau-hs.edu.sa')
    Club.objects.filter(year=year_2015_2016, city='R',
                        gender='F', email='sc-camsf@ksau-hs.edu.sa').update(email='sc-cams-f@ksau-hs.edu.sa')
    Club.objects.filter(year=year_2015_2016, city='R',
                        gender='F', email='sc-cop@ksau-hs.edu.sa').update(email='sc-cop-f@ksau-hs.edu.sa')

class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0031_fill_can_view_assessments'),
    ]

    operations = [
        migrations.RunPython(fix_emails),
    ]
