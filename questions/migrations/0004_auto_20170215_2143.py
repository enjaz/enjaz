# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20170215_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_answer', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=200)),
                ('question', models.ForeignKey(to='questions.Question')),
            ],
        ),
        migrations.RemoveField(
            model_name='answer',
            name='question',
        ),
        migrations.RemoveField(
            model_name='game',
            name='answer',
        ),
        migrations.DeleteModel(
            name='Answer',
        ),
        migrations.AddField(
            model_name='game',
            name='choices',
            field=models.ForeignKey(to='questions.Choice', null=True),
        ),
    ]
