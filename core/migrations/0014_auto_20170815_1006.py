# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0052_presidencies_can_assess'),
        ('core', '0013_campus_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('campus', models.ForeignKey(related_name='colleges', verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629 \u0627\u0644\u062c\u0627\u0645\u0639\u064a\u0629', to='core.Campus')),
                ('old_college_object', models.OneToOneField(related_name='new_college_object', to='clubs.College')),
            ],
            options={
                'verbose_name': '\u0643\u0644\u064a\u0629',
                'verbose_name_plural': '\u0643\u0644\u064a\u0627\u062a',
            },
        ),
        migrations.AlterField(
            model_name='section',
            name='campus',
            field=models.ForeignKey(related_name='sections', verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629 \u0627\u0644\u062c\u0627\u0645\u0639\u064a\u0629', to='core.Campus'),
        ),
        migrations.AddField(
            model_name='college',
            name='section',
            field=models.ForeignKey(related_name='colleges', verbose_name='\u0627\u0644\u0642\u0650\u0633\u0645', to='core.Section'),
        ),
    ]
