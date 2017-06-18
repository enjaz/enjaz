# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0002_add_fonts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='image',
            field=models.ImageField(upload_to=b'certificates', verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629'),
        ),
    ]
