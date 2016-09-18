# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulb', '0019_add_jeddah_alahsa_clubs'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewspaperSignup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(default=b'', max_length=254, blank=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('user', models.OneToOneField(related_name='bulb_newspaper_signup', null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645')),
            ],
        ),
    ]
