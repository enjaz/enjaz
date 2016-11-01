# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub', '0005_add_domain_and_skill'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skilledstudent',
            name='skill',
        ),
        migrations.AddField(
            model_name='skilledstudent',
            name='skill',
            field=models.ManyToManyField(to='researchhub.Skill'),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='domain',
            field=models.ForeignKey(to='researchhub.Domain', null=True),
        ),
    ]
