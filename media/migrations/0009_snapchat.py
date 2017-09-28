# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0008_followupreport_is_draft'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snapchat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_approved', models.NullBooleanField(verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(True, '\u0645\u0639\u062a\u0645\u062f'), (False, '\u0645\u0631\u0641\u0648\u0636'), (None, '\u0645\u0639\u0644\u0642')])),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a', to='clubs.Club', null=True)),
            ],
        ),
    ]
