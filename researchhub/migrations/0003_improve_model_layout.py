# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('researchhub', '0002_add_club'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skilledstudent',
            old_name='skill_description',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='project',
            name='is_available',
        ),
        migrations.RemoveField(
            model_name='supervisor',
            name='is_available',
        ),
        migrations.AddField(
            model_name='project',
            name='communication',
            field=models.TextField(default='', verbose_name=b'Communication method (name/details)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name=b'Is hidden?'),
        ),
        migrations.AddField(
            model_name='project',
            name='is_personal',
            field=models.BooleanField(default=True, help_text=b'Only shown to ReseachHub team members.  Check when this is the personal project of the submitter.', verbose_name=b'Is a personal project?'),
        ),
        migrations.AddField(
            model_name='project',
            name='supervisor',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skilledstudent',
            name='available_from',
            field=models.DateField(help_text=b'Optional', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='skilledstudent',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name=b'Is hidden?'),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='available_from',
            field=models.DateField(help_text=b'Optional', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='available_until',
            field=models.DateField(help_text=b'Optional', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='supervisor',
            name='is_hidden',
            field=models.BooleanField(default=False, verbose_name=b'Is hidden?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(help_text=b'Please write in as much detail as you can.', verbose_name=b'Project description'),
        ),
        migrations.AlterField(
            model_name='project',
            name='duration',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='field',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='prerequisites',
            field=models.TextField(default=b'', help_text=b'What kind of skills do you need in participants? (Optional)', verbose_name=b'Prerequisites', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='required_role',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='skilledstudent',
            name='available_until',
            field=models.DateField(help_text=b'How long are you going to be available? (Optional)', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='skilledstudent',
            name='condition',
            field=models.TextField(help_text=b'Do you have any conditions for joining a research project? (Optional)', blank=True),
        ),
        migrations.AlterField(
            model_name='skilledstudent',
            name='ongoing_projects',
            field=models.TextField(help_text=b'Do you have ongoing projects in which you have used these skills? (Optional)', blank=True),
        ),
        migrations.AlterField(
            model_name='skilledstudent',
            name='previous_experience',
            field=models.TextField(help_text=b'In what projects have you utilized your skills in the past?  (Optional)', blank=True),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='avatar',
            field=models.FileField(help_text=b'Optional', upload_to=b'researchhub/supervisors/', blank=True),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='communication',
            field=models.TextField(verbose_name=b'Communication method'),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='specialty',
            field=models.CharField(max_length=100),
        ),
    ]
