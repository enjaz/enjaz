# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0646\u0634\u0627\u0637')),
                ('description', models.TextField(verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0646\u0634\u0627\u0637')),
                ('public_description', models.TextField(help_text='\u0647\u0630\u0627 \u0647\u0648 \u0627\u0644\u0648\u0635\u0641 \u0627\u0644\u0630\u064a \u0633\u064a\u0639\u0631\u0636 \u0644\u0644\u0637\u0644\u0627\u0628', verbose_name='\u0627\u0644\u0648\u0635\u0641 \u0627\u0644\u0625\u0639\u0644\u0627\u0645\u064a')),
                ('requirements', models.TextField(verbose_name='\u0645\u062a\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0646\u0634\u0627\u0637', blank=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('is_editable', models.BooleanField(default=True, verbose_name='\u0647\u0644 \u064a\u0645\u0643\u0646 \u062a\u0639\u062f\u064a\u0644\u0647\u061f')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('inside_collaborators', models.TextField(verbose_name='\u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0648\u0646 \u0645\u0646 \u062f\u0627\u062e\u0644 \u0627\u0644\u062c\u0627\u0645\u0639\u0629', blank=True)),
                ('outside_collaborators', models.TextField(verbose_name='\u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0648\u0646 \u0645\u0646 \u062e\u0627\u0631\u062c \u0627\u0644\u062c\u0627\u0645\u0639\u0629', blank=True)),
                ('participants', models.IntegerField(help_text='\u0627\u0644\u0639\u062f\u062f \u0627\u0644\u0645\u062a\u0648\u0642\u0639 \u0644\u0644\u0645\u0633\u062a\u0641\u064a\u062f\u064a\u0646 \u0645\u0646 \u0627\u0644\u0646\u0634\u0627\u0637', verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u064a\u0646')),
                ('organizers', models.IntegerField(help_text='\u0639\u062f\u062f \u0627\u0644\u0637\u0644\u0627\u0628 \u0627\u0644\u0630\u064a\u0646 \u0633\u064a\u0646\u0638\u0645\u0648\u0646 \u0627\u0644\u0646\u0634\u0627\u0637', verbose_name='\u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646')),
            ],
            options={
                'verbose_name': '\u0646\u0634\u0627\u0637',
                'verbose_name_plural': '\u0627\u0644\u0646\u0634\u0627\u0637\u0627\u062a',
                'permissions': (('view_activity', 'Can view all available activities.'), ('directly_add_activity', 'Can add activities directly, without approval.')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ar_name', models.CharField(max_length=50, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u062a\u0635\u0646\u064a\u0641')),
                ('en_name', models.CharField(max_length=50, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a')),
                ('description', models.TextField(verbose_name='\u0648\u0635\u0641 \u0627\u0644\u062a\u0635\u0646\u064a\u0641', blank=True)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641 \u0627\u0644\u0623\u0628', blank=True, to='activities.Category', null=True)),
            ],
            options={
                'verbose_name': '\u062a\u0635\u0646\u064a\u0641',
                'verbose_name_plural': '\u0627\u0644\u062a\u0635\u0646\u064a\u0641\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('location', models.CharField(max_length=128)),
                ('allow_multiple_niqati', models.BooleanField(default=False, verbose_name='\u0627\u0633\u0645\u062d \u0628\u0625\u062f\u062e\u0627\u0644 \u0623\u0643\u062b\u0631 \u0645\u0646 \u0631\u0645\u0632 \u0646\u0642\u0627\u0637\u064a\u061f')),
                ('requires_report', models.BooleanField(default=True)),
                ('can_report_early', models.BooleanField(default=False)),
                ('requires_story', models.BooleanField(default=True)),
                ('activity', models.ForeignKey(to='activities.Activity')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quality', models.PositiveIntegerField(help_text='\u0643\u064a\u0641 \u062a\u0642\u064a\u0645 \u0639\u0645\u0644 \u0627\u0644\u0646\u0627\u062f\u064a \u0641\u064a \u062a\u0646\u0638\u064a\u0645 \u0627\u0644\u0646\u0634\u0627\u0637\u061f', verbose_name='\u062c\u0648\u062f\u0629 \u062a\u0646\u0638\u064a\u0645 \u0627\u0644\u0646\u0634\u0627\u0637')),
                ('relevance', models.PositiveIntegerField(help_text='\u0645\u0627 \u0645\u062f\u0649 \u0645\u0644\u0627\u0621\u0645\u0629 \u0627\u0644\u0646\u0634\u0627\u0637 \u0644\u0627\u0647\u062a\u0645\u0627\u0645 \u0627\u0644\u0637\u0644\u0627\u0628\u061f', verbose_name='\u0645\u0644\u0627\u0621\u0645\u0629 \u0627\u0644\u0646\u0634\u0627\u0637 \u0644\u0627\u0647\u062a\u0645\u0627\u0645 \u0627\u0644\u0637\u0644\u0627\u0628')),
                ('episode', models.ForeignKey(to='activities.Episode')),
                ('evaluator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u062a\u0642\u064a\u064a\u0645',
                'verbose_name_plural': '\u0627\u0644\u062a\u0642\u064a\u064a\u0645\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('review_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644', null=True)),
                ('clubs_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u0627\u0644\u0623\u0646\u062f\u064a\u0629', blank=True)),
                ('name_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u0627\u0644\u0627\u0633\u0645', blank=True)),
                ('datetime_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u0627\u0644\u062a\u0627\u0631\u064a\u062e \u0648\u0627\u0644\u0648\u0642\u062a', blank=True)),
                ('description_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u0627\u0644\u0648\u0635\u0641', blank=True)),
                ('requirement_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u0627\u0644\u0645\u062a\u0637\u0644\u0628\u0627\u062a', blank=True)),
                ('inside_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0648\u0646 \u0645\u0646 \u062f\u0627\u062e\u0644 \u0627\u0644\u062c\u0627\u0645\u0639\u0629', blank=True)),
                ('outside_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0648\u0646 \u0645\u0646 \u062e\u0627\u0631\u062c \u0627\u0644\u062c\u0627\u0645\u0639\u0629', blank=True)),
                ('participants_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u0639\u062f\u062f \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u064a\u0646', blank=True)),
                ('organizers_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u0639\u062f\u062f \u0627\u0644\u0645\u0646\u0638\u0645\u064a\u0646', blank=True)),
                ('submission_date_notes', models.TextField(verbose_name='\u0645\u0644\u0627\u062d\u0638\u0627\u062a \u0639\u0644\u0649 \u062a\u0627\u0631\u064a\u062e \u062a\u0642\u062f\u064a\u0645 \u0627\u0644\u0637\u0644\u0628', blank=True)),
                ('review_type', models.CharField(default=b'P', max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629', choices=[(b'P', '\u0631\u0626\u0627\u0633\u0629 \u0646\u0627\u062f\u064a \u0627\u0644\u0637\u0644\u0627\u0628'), (b'D', '\u0639\u0645\u0627\u062f\u0629 \u0634\u0624\u0648\u0646 \u0627\u0644\u0637\u0644\u0627\u0628')])),
                ('is_approved', models.NullBooleanField(verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(None, '\u0623\u0628\u0642\u0650 \u0645\u0639\u0644\u0642\u064b\u0627'), (True, '\u0627\u0642\u0628\u0644'), (False, '\u0627\u0631\u0641\u0636')])),
                ('activity', models.ForeignKey(verbose_name=' \u0627\u0644\u0646\u0634\u0627\u0637', to='activities.Activity')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u0645\u0631\u0627\u062c\u0639\u0629',
                'verbose_name_plural': '\u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0627\u062a',
                'permissions': (('view_review', 'Can view all available reviews.'), ('add_deanship_review', 'Can add a review in the name of the deanship.'), ('add_presidency_review', 'Can add a review in the name of the presidency.'), ('view_deanship_review', 'Can view a review in the name of the deanship.'), ('view_presidency_review', 'Can view a review in the name of the presidency.')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='activity',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641', to='activities.Category', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='primary_club',
            field=models.ForeignKey(related_name='primary_activity', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0645\u0646\u0638\u0645', to='clubs.Club', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='secondary_clubs',
            field=models.ManyToManyField(related_name='secondary_activity', null=True, verbose_name='\u0627\u0644\u0623\u0646\u062f\u064a\u0629 \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u0629', to='clubs.Club', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activity',
            name='submitter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
