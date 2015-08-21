# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('clubs', '0025_assessment'),
        ('core', '0004_studentclubyear_niqati_closure_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0012_fix_attachment_root'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assessment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('notes', models.TextField(verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0646\u0634\u0627\u0637', blank=True)),
                ('activity', models.ForeignKey(to='activities.Activity')),
                ('assessor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('assessor_club', models.ForeignKey(to='clubs.Club', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Criterion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ar_name', models.CharField(max_length=200, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0645\u0639\u064a\u0627\u0631 \u0628\u0627\u0644\u0639\u0631\u0628\u064a\u0629')),
                ('code_name', models.CharField(max_length=200, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0645\u0639\u064a\u0627\u0631 \u0627\u0644\u0628\u0631\u0645\u062c\u064a')),
                ('instructions', models.TextField(verbose_name='\u062a\u0639\u0644\u064a\u0645\u0627\u062a')),
                ('category', models.CharField(max_length=1, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='core.StudentClubYear', null=True, verbose_name='\u0627\u0644\u0633\u0646\u0629')),
            ],
        ),
        migrations.CreateModel(
            name='CriterionValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.IntegerField(verbose_name='\u0627\u0644\u0642\u064a\u0645\u0629')),
                ('assessment', models.ForeignKey(verbose_name='\u0627\u0644\u062a\u0642\u064a\u064a\u0645', to='activities.Assessment')),
                ('criterion', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='activities.Criterion', null=True, verbose_name='\u0627\u0644\u0645\u0639\u064a\u0627\u0631')),
            ],
        ),
        migrations.AlterField(
            model_name='attachment',
            name='description',
            field=models.CharField(max_length=200, verbose_name='\u0627\u0644\u0648\u0635\u0641', blank=True),
        ),
    ]
