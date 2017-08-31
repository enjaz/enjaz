# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0002_auto_20170802_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityRequsetResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_approved', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='activitycancelrequest',
            name='activity',
            field=models.ForeignKey(related_name='requests_canceld', verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', to='activities2.Activity'),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='activity',
            field=models.ForeignKey(related_name='requests_created', verbose_name='\u0627\u0644\u0646\u0634\u0627\u0637', blank=True, to='activities2.Activity', null=True),
        ),
        migrations.AddField(
            model_name='activityrequsetresponse',
            name='activity_request',
            field=models.ForeignKey(related_name='activityrequsetresponses', verbose_name='\u0637\u0644\u0628 \u0627\u0644\u0646\u0634\u0627\u0637', to='approvals.ActivityRequest'),
        ),
        migrations.AddField(
            model_name='activityrequsetresponse',
            name='request',
            field=models.ForeignKey(to='approvals.ActivityRequest'),
        ),
    ]
