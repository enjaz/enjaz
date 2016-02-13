# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_studentclubyear_niqati_closure_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field', models.CharField(max_length=100, verbose_name=b'Field')),
                ('title', models.CharField(max_length=255, verbose_name=b'Title')),
                ('description', models.TextField(verbose_name='Project description')),
                ('required_role', models.TextField(verbose_name='Required role')),
                ('prerequisites', models.TextField(default=b'', verbose_name='Required role', blank=True)),
                ('duration', models.CharField(max_length=100, verbose_name=b'Duration')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('is_available', models.BooleanField(default=True, verbose_name=b'Is available?')),
                ('is_deleted', models.BooleanField(default=False, verbose_name=b'Is deleted?')),
                ('submitter', models.ForeignKey(related_name='submitted_research_projects', to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.StudentClubYear', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SkilledStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('skill_description', models.TextField(help_text=b'Describe your skills in as much detail as you can.')),
                ('previous_experience', models.TextField(help_text=b'In what projects have you utilized your skills in the past?', blank=True)),
                ('ongoing_projects', models.TextField(help_text=b'Do you have ongoing projects in which you have used these skills?', blank=True)),
                ('condition', models.TextField(help_text=b'What are your conditions for joining a research project?')),
                ('available_until', models.DateField(null=True, blank=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False, verbose_name=b'Is deleted?')),
                ('user', models.ForeignKey(related_name='researchhub_skill_profiles', to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.StudentClubYear', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Supervisor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('specialty', models.CharField(max_length=100, verbose_name=b'Specialty')),
                ('avatar', models.FileField(upload_to=b'researchhub/supervisors/', verbose_name=b'Avatar')),
                ('position', models.CharField(max_length=100, verbose_name=b'Position/Title')),
                ('interests', models.TextField(verbose_name='Research areas of interest')),
                ('communication', models.CharField(max_length=255, verbose_name=b'Communication method')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now=True)),
                ('is_available', models.BooleanField(default=True, verbose_name=b'Is available?')),
                ('is_deleted', models.BooleanField(default=False, verbose_name=b'Is deleted?')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.StudentClubYear', null=True)),
            ],
        ),
    ]
