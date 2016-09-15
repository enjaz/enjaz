# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_add_2016_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=155, verbose_name='\u0627\u0644\u0646\u0635')),
                ('tweet_id', models.BigIntegerField(null=True)),
                ('was_sent', models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u062a\u061f')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0636\u0627\u0641\u0629')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
