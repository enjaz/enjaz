# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studentguide', '0008_optional_other_comments'),
    ]

    operations = [
        migrations.CreateModel(
            name='MentorOfTheMonth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('month', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0634\u0647\u0631')),
                ('gender', models.CharField(max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u062f\u0631')),
                ('avatar', models.ImageField(upload_to=b'studentguide/mentor_of_the_month/', verbose_name='\u0635\u0648\u0631\u0629 \u0631\u0645\u0632\u064a\u0629')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0634\u062f \u0627\u0644\u0637\u0644\u0627\u0628\u064a', to='studentguide.GuideProfile', null=True)),
            ],
        ),
    ]
