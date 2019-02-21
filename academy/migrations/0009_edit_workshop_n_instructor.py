# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0008_edit_media_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='course',
            field=models.ManyToManyField(related_name='course_instructors', verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629', to='academy.SubCourse', blank=True),
        ),
        migrations.AlterField(
            model_name='instructor',
            name='workshop',
            field=models.ManyToManyField(related_name='workshop_instructors', verbose_name='\u0648\u0631\u0634\u0629 \u0627\u0644\u0639\u0645\u0644', to='academy.Workshop', blank=True),
        ),
    ]
