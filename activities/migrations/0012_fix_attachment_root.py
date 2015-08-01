# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0011_activity_chosen_reviewer_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='document',
            field=models.FileField(upload_to=b'activity_attachments/', verbose_name='\u0627\u0644\u0645\u0633\u062a\u0646\u062f'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='preview',
            field=models.FileField(upload_to=b'activity_attachment_previews/', verbose_name='\u0645\u0639\u0627\u064a\u0646\u0629'),
        ),
    ]
