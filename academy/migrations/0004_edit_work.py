# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0003_beauty_n_convenience'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media_File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to='academy/photos_n_projects', null=True, verbose_name='\u0627\u0644\u0645\u0644\u0641', blank=True)),
                ('subcourse', models.ForeignKey(related_name='subcourse_media', verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629 \u0627\u0644\u062a\u0627\u0628\u0639\u0629', to='academy.SubCourse')),
            ],
            options={
                'verbose_name': '\u0645\u0631\u0641\u0642',
                'verbose_name_plural': '\u0627\u0644\u0645\u0631\u0641\u0642\u0627\u062a',
            },
        ),
        migrations.RemoveField(
            model_name='work',
            name='done_projects',
        ),
        migrations.RemoveField(
            model_name='work',
            name='projects_in_sc',
        ),
        migrations.RemoveField(
            model_name='work',
            name='projects_outside_sc',
        ),
        migrations.AddField(
            model_name='work',
            name='instructor',
            field=models.ManyToManyField(to='academy.Instructor', verbose_name='\u0627\u0644\u0645\u0634\u0631\u0641\u0640/\u0640\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='work',
            name='type',
            field=models.CharField(blank=True, max_length=2, null=True, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0639\u0645\u0644', choices=[('in', '\u062f\u0627\u062e\u0644 \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628'), ('out', '\u062e\u0627\u0631\u062c \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628')]),
        ),
        migrations.AlterField(
            model_name='work',
            name='graduate',
            field=models.ManyToManyField(to='academy.Graduate', verbose_name='\u0627\u0644\u062e\u0631\u064a\u062c\u0640/\u0640\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='work',
            name='attachments',
            field=models.ManyToManyField(to='academy.Media_File', verbose_name='\u0645\u0631\u0641\u0642\u0627\u062a', blank=True),
        ),
    ]
