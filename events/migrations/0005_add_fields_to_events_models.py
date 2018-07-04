# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_presentaion_date_not_required'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='logo',
            field=models.FileField(upload_to=b'events/logos/', null=True, verbose_name='Attach the event logo', blank=True),
        ),
        migrations.AddField(
            model_name='session',
            name='image',
            field=models.FileField(upload_to=b'events/sessions/', null=True, verbose_name='Attach the speaker image to be displayed', blank=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='image',
            field=models.FileField(upload_to=b'events/timeslots/', null=True, verbose_name='Attach the schedule to be displayed', blank=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='limit',
            field=models.PositiveSmallIntegerField(default=None, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='parent',
            field=models.ForeignKey(related_name='children', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='events.TimeSlot', null=True, verbose_name='\u0627\u0644\u0642\u0633\u0645 \u0627\u0644\u0623\u0628'),
        ),
    ]
