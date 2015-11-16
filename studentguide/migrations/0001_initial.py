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
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0645\u062d\u0636\u0631')),
            ],
        ),
        migrations.CreateModel(
            name='GuideProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('avatar', models.ImageField(upload_to=b'studentguide/avatar/', verbose_name='\u0635\u0648\u0631\u0629 \u0631\u0645\u0632\u064a\u0629')),
                ('activities', models.TextField(help_text='\u0645\u0627 \u0623\u0628\u0631\u0632 \u0627\u0644\u0623\u0646\u0634\u0637\u0629 \u0648\u0627\u0644\u0645\u0634\u0627\u0631\u064a\u0639 \u0627\u0644\u062a\u064a \u0633\u0628\u0642 \u0623\u0646 \u0639\u0645\u0644\u062a \u0639\u0644\u064a\u0647\u0627\u061f \u0647\u0630\u0627 \u064a\u062a\u0636\u0645\u0646 \u0623\u064a \u0623\u0628\u062d\u0627\u062b\u060c \u0623\u0648 \u0623\u0639\u0645\u0627\u0644 \u0643\u0627\u0646 \u0644\u0643 \u062f\u0648\u0631\u064c \u0623\u0633\u0627\u0633\u064a\u064c \u0641\u064a\u0647\u0627.', verbose_name='\u0627\u0644\u0645\u0634\u0627\u0631\u064a\u0639 \u0648\u0627\u0644\u0646\u0634\u0627\u0637\u0627\u062a \u0627\u0644\u0633\u0627\u0628\u0642\u0629')),
                ('academic_interests', models.TextField(help_text='\u0641\u064a \u0627\u0644\u0633\u064a\u0627\u0642 \u0627\u0644\u0623\u0643\u0627\u062f\u064a\u0645\u064a\u060c \u0645\u0627 \u0627\u0644\u0630\u064a \u064a\u0633\u062a\u0647\u0648\u064a\u0643\u061f', verbose_name='\u0627\u0644\u0627\u0647\u062a\u0645\u0627\u0645\u0627\u062a \u0627\u0644\u0623\u0643\u0627\u062f\u064a\u0645\u064a\u0629')),
                ('nonacademic_interests', models.TextField(help_text='\u0628\u0639\u064a\u062f\u0627 \u0639\u0646 \u0627\u0644\u062a\u062d\u0635\u064a\u0644 \u0627\u0644\u0623\u0643\u0627\u062f\u064a\u0645\u064a\u060c \u0645\u0627 \u0627\u0644\u0630\u064a \u064a\u0634\u063a\u0644\u0643\u061f', verbose_name='\u0627\u0644\u0627\u0647\u062a\u0645\u0627\u0645\u0627\u062a \u063a\u064a\u0631  \u0627\u0644\u0623\u0643\u0627\u062f\u064a\u0645\u064a\u0629')),
                ('batch', models.PositiveSmallIntegerField(verbose_name='\u0627\u0644\u062f\u0641\u0639\u0629')),
                ('is_available', models.BooleanField(default=True, verbose_name='\u0645\u062a\u0627\u062d\u061f')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
            ],
            options={
                'verbose_name': '\u0645\u0644\u0641 \u0645\u0631\u0634\u062f \u0637\u0644\u0627\u0628\u064a',
                'verbose_name_plural': '\u0645\u0644\u0641\u0627\u062a \u0627\u0644\u0645\u0631\u0634\u062f\u064a\u0646 \u0627\u0644\u0637\u0644\u0627\u0628\u064a\u064a\u0646',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0645\u062d\u0636\u0631')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('was_revised', models.BooleanField(default=False, verbose_name='\u0631\u0648\u062c\u0639\u061f')),
                ('revision_date', models.DateTimeField(default=None, null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('guide', models.ForeignKey(related_name='student_guide_reports', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0634\u062f \u0627\u0644\u0637\u0644\u0627\u0628\u064a', to='studentguide.GuideProfile', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guide_status', models.CharField(default=b'P', max_length=1, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629 \u0627\u0644\u0645\u0631\u0634\u062f', choices=[(b'P', '\u0645\u0639\u0644\u0642'), (b'A', '\u0645\u0642\u0628\u0648\u0644'), (b'R', '\u0645\u0631\u0641\u0648\u0636')])),
                ('guide_status_date', models.DateTimeField(default=None, null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u062d\u0627\u0644\u0629 \u0627\u0644\u0645\u0631\u0634\u062f', blank=True)),
                ('requester_status', models.CharField(default=b'A', max_length=1, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629 \u0645\u0642\u062f\u0645 \u0627\u0644\u0637\u0644\u0628', choices=[(b'A', '\u0645\u0639\u062a\u0645\u062f\u0629'), (b'C', '\u0645\u0644\u063a\u0627\u0629')])),
                ('interests', models.TextField(help_text='\u0645\u0627 \u0627\u0644\u0645\u062c\u0627\u0644\u0627\u062a \u0627\u0644\u062a\u064a \u062a\u0631\u064a\u062f \u062a\u0637\u0648\u064a\u0631 \u0646\u0641\u0633\u0643 \u0641\u064a\u0647\u0627\u061f', verbose_name='\u0627\u0644\u0627\u0647\u062a\u0645\u0627\u0645\u0627\u062a')),
                ('batch', models.PositiveSmallIntegerField(verbose_name='\u0627\u0644\u062f\u0641\u0639\u0629')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('guide', models.ForeignKey(related_name='guide_requests', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0634\u062f \u0627\u0644\u0637\u0644\u0627\u0628\u064a', to='studentguide.GuideProfile', null=True)),
                ('user', models.ForeignKey(related_name='guide_requests', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0637\u0627\u0644\u0628 \u0627\u0644\u0645\u0633\u062a\u062c\u062f', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u0637\u0644\u0628 \u0625\u0631\u0634\u0627\u062f',
                'verbose_name_plural': '\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0625\u0631\u0634\u0627\u062f',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('code_name', models.CharField(help_text='\u062d\u0631\u0648\u0641 \u0644\u0627\u062a\u064a\u0646\u064a\u0629 \u0635\u063a\u064a\u0631\u0629 \u0648\u0623\u0631\u0642\u0627\u0645', max_length=50, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0628\u0631\u0645\u062c\u064a')),
            ],
        ),
        migrations.AddField(
            model_name='guideprofile',
            name='tags',
            field=models.ManyToManyField(related_name='guide_profiles', verbose_name='\u0627\u0644\u0648\u0633\u0648\u0645', to='studentguide.Tag'),
        ),
        migrations.AddField(
            model_name='guideprofile',
            name='user',
            field=models.ForeignKey(related_name='guide_profiles', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='guideprofile',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, verbose_name='\u0627\u0644\u0633\u0646\u0629', to='core.StudentClubYear', null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0634\u062f \u0627\u0644\u0637\u0644\u0627\u0628\u064a', to='studentguide.GuideProfile', null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='submitter',
            field=models.ForeignKey(related_name='arshidni_feedback', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
