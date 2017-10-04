# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approvals', '0005_auto_20170913_0608'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0648\u0635\u0641')),
                ('file', models.FileField(upload_to=b'approvals/file_attachments/', verbose_name='\u0627\u0644\u0645\u0644\u0641')),
            ],
            options={
                'verbose_name': '\u0645\u0644\u0641 \u0645\u0631\u0641\u0642',
                'verbose_name_plural': '\u0645\u0644\u0641\u0627\u062a \u0645\u0631\u0641\u0642\u0629',
            },
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='campus',
            field=models.ManyToManyField(to='core.Campus', verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629 \u0627\u0644\u062c\u0627\u0645\u0639\u064a\u0629'),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='category',
            field=models.CharField(max_length=50, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641'),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='gender',
            field=models.CharField(max_length=1, verbose_name='\u0627\u0644\u0642\u0633\u0645', choices=[(b'M', '\u0627\u0644\u0637\u0644\u0627\u0628'), (b'F', '\u0627\u0644\u0637\u0627\u0644\u0628\u0627\u062a')]),
        ),
        migrations.AlterField(
            model_name='activityrequest',
            name='specialty',
            field=models.ManyToManyField(to='core.Specialty', verbose_name='\u0627\u0644\u062a\u062e\u0635\u0635'),
        ),
        migrations.AddField(
            model_name='fileattachment',
            name='activity_request',
            field=models.ForeignKey(related_name='fileattachments', verbose_name='\u0637\u0644\u0628 \u0627\u0644\u0646\u0634\u0627\u0637', to='approvals.ActivityRequest'),
        ),
    ]
