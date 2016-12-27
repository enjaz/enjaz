# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub', '0007_add_data_to_domain_and_skill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skilledstudent',
            name='skill',
        ),
        migrations.AddField(
            model_name='skilledstudent',
            name='skills',
            field=models.ManyToManyField(to='researchhub.Skill', verbose_name='\u0627\u0644\u0645\u0647\u0627\u0631\u0629'),
        ),
    ]
