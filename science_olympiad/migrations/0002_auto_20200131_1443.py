# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('science_olympiad', '0001_add_question_n_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0645\u0633\u0627\u0628\u0642\u0629')),
                ('teams', models.TextField(null=True, verbose_name='\u0627\u0644\u0641\u0650\u0631\u0642 \u0627\u0644\u0645\u0646\u0627\u0641\u0650\u0633\u0629', blank=True)),
            ],
            options={
                'verbose_name': '\u0645\u0633\u0627\u0628\u0642\u0629',
                'verbose_name_plural': '\u0645\u0633\u0627\u0628\u0642\u0627\u062a',
            },
        ),
        migrations.AlterField(
            model_name='contestquestion',
            name='category',
            field=models.CharField(max_length=100, verbose_name='\u0627\u0644\u0641\u0626\u0629'),
        ),
        migrations.AddField(
            model_name='contestquestion',
            name='contest',
            field=models.ForeignKey(default='', verbose_name='\u0627\u0644\u0645\u0633\u0627\u0628\u0642\u0629', to='science_olympiad.Contest'),
        ),
    ]
