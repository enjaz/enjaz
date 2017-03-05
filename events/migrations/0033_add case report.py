# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0032_auto_20170303_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaseReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('authors', models.TextField(verbose_name='Name of authors')),
                ('study_field', models.CharField(default=b'', max_length=255, verbose_name=b'Field')),
                ('university', models.CharField(max_length=255, verbose_name=b'University')),
                ('college', models.CharField(max_length=255, verbose_name=b'College')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email')),
                ('phone', models.CharField(max_length=20, verbose_name=b'Phone number')),
                ('introduction', models.TextField(default=b'', verbose_name='Introduction')),
                ('patient_info', models.TextField(default=b'', verbose_name='Patient info')),
                ('clinical_presentation', models.TextField(default=b'', verbose_name='clinical presentation')),
                ('diagnosis', models.TextField(default=b'', verbose_name='Diagnosis')),
                ('treatment', models.TextField(default=b'', verbose_name='Treatment')),
                ('outcome', models.TextField(default=b'', verbose_name='Outcome')),
                ('discussion', models.TextField(default=b'', verbose_name='Discussion')),
                ('conclusion', models.TextField(default=b'', verbose_name='Conclusion')),
                ('was_published', models.BooleanField(default=False, verbose_name='Have you published this research?')),
                ('was_presented_at_others', models.BooleanField(default=False, verbose_name='Have you presented this research in any other conference before?')),
                ('was_presented_previously', models.BooleanField(default=False, verbose_name='Have you presented this research in a previous year of this conference?')),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('event', models.ForeignKey(verbose_name='\u0627\u0644\u062d\u062f\u062b', to='events.Event')),
                ('user', models.ForeignKey(related_name='event_casereport', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
