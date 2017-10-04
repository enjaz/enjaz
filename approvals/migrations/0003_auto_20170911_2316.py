# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0002_auto_20170802_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityRequestReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_approved', models.BooleanField(verbose_name='\u062a\u0645 \u0627\u0644\u0627\u0639\u062a\u0645\u0627\u062f\u061f', choices=[(True, '\u0646\u0639\u0645'), (False, '\u0644\u0627')])),
                ('review_datetime', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0648 \u0648\u0642\u062a \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629')),
            ],
        ),
        migrations.AddField(
            model_name='activityrequest',
            name='thread_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
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
            model_name='activityrequestreview',
            name='request',
            field=models.ForeignKey(related_name='reviews', verbose_name='\u0637\u0644\u0628 \u0627\u0644\u0646\u0634\u0627\u0637', to='approvals.ActivityRequest'),
        ),
    ]
