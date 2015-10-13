# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arshidni', '0006_fill_colleague_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0645\u062d\u0636\u0631')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0645\u062d\u0636\u0631')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('was_revised', models.BooleanField(default=False, verbose_name='\u0631\u0648\u062c\u0639\u061f')),
                ('revision_date', models.DateTimeField(default=None, null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
        ),
        migrations.AlterModelOptions(
            name='colleagueprofile',
            options={'verbose_name': '\u0645\u0644\u0641 \u0645\u0631\u0634\u062f \u0637\u0644\u0627\u0628\u064a', 'verbose_name_plural': '\u0645\u0644\u0641\u0627\u062a \u0627\u0644\u0645\u0631\u0634\u062f\u064a\u0646 \u0627\u0644\u0637\u0644\u0627\u0628\u064a\u064a\u0646'},
        ),
        migrations.AlterModelOptions(
            name='supervisionrequest',
            options={'verbose_name': '\u0637\u0644\u0628 \u0625\u0631\u0634\u0627\u062f', 'verbose_name_plural': '\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0625\u0631\u0634\u0627\u062f'},
        ),
        migrations.AlterField(
            model_name='supervisionrequest',
            name='colleague',
            field=models.ForeignKey(related_name='supervision_requests', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0634\u062f \u0627\u0644\u0637\u0644\u0627\u0628\u064a', to='arshidni.ColleagueProfile', null=True),
        ),
        migrations.AlterField(
            model_name='supervisionrequest',
            name='status',
            field=models.CharField(default=b'P', max_length=2, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(b'P', '\u062a\u0646\u062a\u0638\u0631 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629'), (b'A', '\u0645\u0642\u0628\u0648\u0644'), (b'R', '\u0645\u0631\u0641\u0648\u0636'), (b'D', '\u0623\u0644\u063a\u0627\u0647 \u0627\u0644\u0637\u0627\u0644\u0628 \u0627\u0644\u0645\u0633\u062a\u062c\u062f \u0642\u0628\u0644 \u0623\u0646 \u064a\u0631\u0627\u062c\u0639\u0647 \u0627\u0644\u0645\u0631\u0634\u062f \u0627\u0644\u0637\u0644\u0627\u0628\u064a'), (b'WN', '\u0623\u0644\u063a\u0627\u0647 \u0627\u0644\u0637\u0627\u0644\u0628 \u0627\u0644\u0645\u0633\u062a\u062c\u062f'), (b'WC', '\u0623\u0644\u063a\u0627\u0647 \u0627\u0644\u0645\u0631\u0634\u062f \u0627\u0644\u0637\u0644\u0627\u0628\u064a')]),
        ),
        migrations.AddField(
            model_name='report',
            name='colleague',
            field=models.ForeignKey(related_name='student_guide_reports', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0634\u062f \u0627\u0644\u0637\u0644\u0627\u0628\u064a', to='arshidni.ColleagueProfile', null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='colleague',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0634\u062f \u0627\u0644\u0637\u0644\u0627\u0628\u064a', to='arshidni.ColleagueProfile', null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='submitter',
            field=models.ForeignKey(related_name='student_guide_feedback', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='colleagueprofile',
            name='tags',
            field=models.ManyToManyField(related_name='colleague_profiles', verbose_name='\u0627\u0644\u0648\u0633\u0648\u0645', to='arshidni.Tag'),
        ),
    ]
