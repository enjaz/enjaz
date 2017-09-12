# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0003_edit_teams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='coordinator',
        ),
        migrations.AddField(
            model_name='teams',
            name='leader',
            field=models.ForeignKey(related_name='teams_leader', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0646\u0633\u0642', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='teams',
            name='logo',
            field=models.ImageField(null=True, upload_to=b'teams/logos/', blank=True),
        ),
        migrations.AlterField(
            model_name='teams',
            name='members',
            field=models.ManyToManyField(related_name='teams', verbose_name='\u0627\u0644\u0623\u0639\u0636\u0627\u0621', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
