# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub', '0004_remove_supervisor_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to=b'researchhub/domain/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('image', models.FileField(upload_to=b'researchhub/skill/', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='specialty',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='skilledstudent',
            name='skill',
            field=models.ForeignKey(default=b'', to='researchhub.Skill'),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='domain',
            field=models.ForeignKey(default=b'', to='researchhub.Domain'),
        ),
    ]
