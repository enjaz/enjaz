# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0053_be_nice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0646\u0635 \u0627\u0644\u0633\u0624\u0627\u0644')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, verbose_name='\u0639\u0646\u0648\u0627\u0646 \u0627\u0644\u062c\u0644\u0633\u0629')),
                ('event', models.ForeignKey(verbose_name=b'\xd8\xa7\xd9\x84\xd8\xad\xd8\xaf\xd8\xab', to='events.Event')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='question_session',
            field=models.ForeignKey(verbose_name=b'\xd8\xac\xd9\x84\xd8\xb3\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb3\xd8\xa4\xd8\xa7\xd9\x84', to='events.QuestionSession'),
        ),
    ]
