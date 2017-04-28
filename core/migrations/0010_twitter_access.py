# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_tweet_failed_trials'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterAccess',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_token', models.CharField(max_length=200)),
                ('access_token_secret', models.CharField(max_length=200)),
                ('code_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='tweet',
            name='access',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.TwitterAccess', null=True),
        ),
    ]
