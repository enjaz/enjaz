# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub', '0008_improve_skills_many_to_many'),
    ]

    operations = [
        migrations.AddField(
            model_name='domain',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='skill',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='skilledstudent',
            name='skills',
            field=models.ManyToManyField(help_text=b'Hold down (Control), or (Command) on a Mac, to select more than one.', to='researchhub.Skill'),
        ),
    ]
