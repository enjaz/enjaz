# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0040_event_extra_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractPoster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('poster', models.FileField(upload_to=b'events/posters/', verbose_name='Attach the poster')),
                ('poster_powerpoint', models.FileField(upload_to=b'events/poster_powerpoints/', verbose_name='Attach the poster powerpoint')),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='abstract',
            name='status',
            field=models.CharField(default=b'P', max_length=1, verbose_name=b'acceptance status', choices=[(b'A', b'Accepted'), (b'P', b'Pending'), (b'R', b'Rejected')]),
        ),
        migrations.AddField(
            model_name='abstractposter',
            name='abstract',
            field=models.ForeignKey(related_name='posters', to='events.Abstract', null=True),
        ),
    ]
