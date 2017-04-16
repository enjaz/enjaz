# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tedx', '0003_registration_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice_text', models.CharField(default='\u062e\u064a\u0627\u0631', max_length=3159)),
                ('title', models.CharField(default='choice title', max_length=30)),
                ('icon', models.CharField(max_length=30, blank=True)),
                ('flag', models.CharField(default='choice title', max_length=30, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_text', models.TextField(default='question text', verbose_name='\u0646\u0635 \u0627\u0644\u0633\u0624\u0627\u0644')),
                ('title', models.CharField(default='question title', max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='first_question',
            field=models.ForeignKey(to='tedx.Question'),
        ),
        migrations.AddField(
            model_name='choice',
            name='next_question',
            field=models.ForeignKey(related_name='leading_choices', to='tedx.Question', null=True),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(related_name='choices', to='tedx.Question'),
        ),
    ]
