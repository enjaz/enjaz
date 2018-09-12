# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0001_create_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexBG',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('img', models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629 ')),
            ],
            options={
                'verbose_name': '\u0635\u0648\u0631\u0629 \u062e\u0644\u0641\u064a\u0629',
                'verbose_name_plural': '\u0627\u0644\u0635\u0648\u0631 \u0627\u0644\u062e\u0644\u0641\u064a\u0629',
            },
        ),
    ]
