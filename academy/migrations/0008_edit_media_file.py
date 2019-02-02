# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0007_add_workshop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media_file',
            name='subcourse',
            field=models.ForeignKey(related_name='subcourse_media', verbose_name='\u0627\u0644\u062f\u0648\u0631\u0629 \u0627\u0644\u062a\u0627\u0628\u0639\u0629', blank=True, to='academy.SubCourse', null=True),
        ),
    ]
