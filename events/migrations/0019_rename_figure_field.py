# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_merge'),
    ]

    operations = [
        migrations.RenameField(
            model_name='abstractfigure',
            old_name='figure',
            new_name='upload',
        ),
        migrations.AlterField(
            model_name='abstractfigure',
            name='abstract',
            field=models.ForeignKey(related_name='figures', to='events.Abstract', null=True),
        ),
    ]
