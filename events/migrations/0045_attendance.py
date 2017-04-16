# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0044_add_second_poster_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(blank=True, max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u062a\u062d\u0636\u064a\u0631', choices=[(b'I', '\u0627\u0644\u062f\u062e\u0648\u0644'), (b'M', '\u0627\u0644\u0645\u0646\u062a\u0635\u0641'), (b'O', '\u0627\u0644\u062e\u0631\u0648\u062c')])),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('session', models.ForeignKey(to='events.Session')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
