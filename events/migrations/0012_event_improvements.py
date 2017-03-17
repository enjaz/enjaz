# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clubs', '0046_add_jeddah_ams_deanship'),
        ('events', '0011_better_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='Abstract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('authors', models.TextField(verbose_name='Name of authors')),
                ('university', models.CharField(max_length=255, verbose_name=b'University')),
                ('college', models.CharField(max_length=255, verbose_name=b'College')),
                ('presenting_author', models.CharField(max_length=255, verbose_name=b'Presenting author')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email')),
                ('phone', models.CharField(max_length=20, verbose_name=b'Phone number')),
                ('level', models.CharField(default=b'', max_length=1, verbose_name=b'Level', choices=[(b'U', b'Undergraduate'), (b'G', b'Graduate')])),
                ('presentation_preference', models.CharField(max_length=1, verbose_name=b'Presentation preference', choices=[(b'O', b'Oral'), (b'P', b'Poster')])),
                ('attachment', models.FileField(upload_to=b'hpc/abstract/', verbose_name='Attach the abstract')),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
            ],
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('human_name', models.CharField(max_length=200, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0645\u0639\u064a\u0627\u0631 \u0627\u0644\u0630\u064a \u0633\u064a\u0638\u0647\u0631')),
                ('code_name', models.CharField(max_length=200, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0645\u0639\u064a\u0627\u0631 \u0627\u0644\u0628\u0631\u0645\u062c\u064a')),
                ('instructions', models.TextField(verbose_name='\u062a\u0639\u0644\u064a\u0645\u0627\u062a')),
            ],
        ),
        migrations.CreateModel(
            name='CriterionValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(verbose_name='\u0627\u0644\u0642\u064a\u0645\u0629')),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='events.Criterion', null=True, verbose_name='\u0627\u0644\u0645\u0639\u064a\u0627\u0631')),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('abstract', models.ForeignKey(to='events.Abstract')),
                ('evaluator', models.ForeignKey(related_name='event_abstract_evaluations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='event',
            old_name="is_english_name",
            new_name="is_official_name_english"),
        migrations.RenameField(
            model_name='event',
            old_name="name",
            new_name="official_name"),
        migrations.AddField(
            model_name='event',
            name='abstract_revision_club',
            field=models.ForeignKey(related_name='abstract_revision_events', blank=True, to='clubs.Club', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='abstract_submission_closing_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0646\u062a\u0647\u0627\u0621 \u0625\u063a\u0644\u0627\u0642 \u0627\u0633\u062a\u0642\u0628\u0627\u0644 \u0627\u0644\u0645\u0644\u062e\u0635\u0627\u062a \u0627\u0644\u0628\u062d\u062b\u064a\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='abstract_submission_instruction_url',
            field=models.URLField(default=b'', max_length=255, verbose_name='\u0631\u0627\u0628\u0637 \u062a\u0639\u0644\u064a\u0645\u0627\u062a \u0625\u0631\u0633\u0627\u0644 \u0627\u0644\u0623\u0628\u062d\u0627\u062b', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='abstract_submission_opening_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0641\u062a\u062d \u0627\u0633\u062a\u0642\u0628\u0627\u0644 \u0627\u0644\u0645\u0644\u062e\u0635\u0627\u062a \u0627\u0644\u0628\u062d\u062b\u064a\u0629', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='english_name',
            field=models.CharField(default=b'', max_length=255, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='is_official_name_english',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0633\u0645 \u0627\u0644\u062d\u062f\u062b \u0627\u0644\u0631\u0633\u0645\u064a \u0625\u0646\u062c\u0644\u064a\u0632\u064a'),
        ),
        migrations.AlterField(
            model_name='event',
            name='official_name',
            field=models.CharField(default='', max_length=255, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0631\u0633\u0645\u064a'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='receives_abstract_submission',
            field=models.BooleanField(default=False, verbose_name='\u064a\u0633\u062a\u0642\u0628\u0644 \u0645\u0644\u062e\u0635\u0627\u062a \u0628\u062d\u062b\u064a\u0629\u061f'),
        ),
        migrations.AlterField(
            model_name='event',
            name='onsite_after',
            field=models.DateTimeField(null=True, verbose_name='\u0627\u0644\u062a\u0633\u062c\u064a\u0644 \u0641\u064a \u0627\u0644\u0645\u0648\u0642\u0639 \u064a\u0628\u062f\u0623 \u0645\u0646', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_closing_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0646\u062a\u0647\u0627\u0621 \u0627\u0644\u062a\u0633\u062c\u064a\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='registration_opening_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0641\u062a\u062d \u0627\u0644\u062a\u0633\u062c\u064a\u0644', blank=True),
        ),
        migrations.AddField(
            model_name='criterionvalue',
            name='evaluation',
            field=models.ForeignKey(related_name='criterion_values', verbose_name='\u0627\u0644\u062a\u0642\u064a\u064a\u0645', to='events.Evaluation'),
        ),
        migrations.AddField(
            model_name='criterion',
            name='event',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u062d\u062f\u062b', to='events.Event', null=True),
        ),
        migrations.AddField(
            model_name='abstract',
            name='event',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u062d\u062f\u062b', to='events.Event'),
        ),
    ]
