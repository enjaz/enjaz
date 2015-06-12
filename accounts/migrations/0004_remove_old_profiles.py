# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_create_common_profiles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nonstudentprofile',
            name='enjazbaseprofile_ptr',
        ),
        migrations.RemoveField(
            model_name='nonstudentprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='college',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='enjazbaseprofile_ptr',
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='user',
        ),
        migrations.DeleteModel(
            name='EnjazBaseProfile',
        ),
        migrations.DeleteModel(
            name='NonStudentProfile',
        ),
        migrations.DeleteModel(
            name='StudentProfile',
        ),
    ]
