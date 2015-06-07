# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0646\u0635')),
                ('is_published', models.NullBooleanField(default=True, verbose_name='\u0645\u0646\u0634\u0648\u0631\u061f', choices=[(None, '\u0644\u0645 \u064a\u0631\u0627\u062c\u0639 \u0628\u0639\u062f'), (True, '\u0645\u0646\u0634\u0648\u0631'), (False, '\u0645\u062d\u0630\u0648\u0641')])),
                ('is_editable', models.BooleanField(default=True, verbose_name='\u064a\u0645\u0643\u0646 \u062a\u0639\u062f\u064a\u0644\u0647\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='arshidni.Answer', null=True, verbose_name='\u0627\u0644\u062a\u0639\u0644\u064a\u0642 \u0627\u0644\u0623\u0628')),
            ],
            options={
                'verbose_name': '\u0625\u062c\u0627\u0628\u0629',
                'verbose_name_plural': '\u0627\u0644\u0625\u062c\u0627\u0628\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArshidniProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interests', models.TextField(help_text='\u0645\u0627 \u0647\u064a \u0627\u0647\u062a\u0645\u0627\u0645\u062a\u0643 \u0627\u0644\u0623\u0643\u0627\u062f\u064a\u0645\u064a\u0629\u061f', verbose_name='\u0627\u0644\u0627\u0647\u062a\u0645\u0627\u0645\u0627\u062a')),
                ('contacts', models.CharField(help_text='\u062c\u0648\u0627\u0644 \u0645\u062b\u0644\u0627\u061f', max_length=100, verbose_name='\u0637\u0631\u064a\u0642\u0629 \u0627\u0644\u062a\u0648\u0627\u0635\u0644')),
                ('is_published', models.NullBooleanField(default=True, verbose_name='\u0645\u0646\u0634\u0648\u0631\u061f', choices=[(None, '\u0644\u0645 \u064a\u0631\u0627\u062c\u0639 \u0628\u0639\u062f'), (True, '\u0645\u0646\u0634\u0648\u0631'), (False, '\u0645\u062d\u0630\u0648\u0641')])),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ColleagueProfile',
            fields=[
                ('arshidniprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='arshidni.ArshidniProfile')),
                ('bio', models.TextField(help_text='\u0647\u0644 \u062e\u0636\u062a \u0623\u064a \u0627\u062e\u062a\u0628\u0627\u0631\u0627\u062a \u0639\u0627\u0644\u0645\u064a\u0629\u061f \u0647\u0644 \u062a\u062f\u0631\u0628\u062a \u0641\u064a \u0645\u0633\u062a\u0634\u0641\u0649\u061f \u0647\u0644 \u0634\u0627\u0631\u0643\u062a \u0641\u064a \u0623\u0628\u062d\u0627\u062b\u061f', verbose_name='\u0646\u0628\u0630\u0629')),
                ('batch', models.PositiveSmallIntegerField(verbose_name='\u0627\u0644\u062f\u0641\u0639\u0629')),
                ('is_available', models.BooleanField(default=True, verbose_name='\u0647\u0644 \u0647\u0648 \u0645\u062a\u0627\u062d\u061f')),
                ('user', models.OneToOneField(related_name='colleague_profile', null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0645\u0644\u0641 \u0632\u0645\u064a\u0644 \u0637\u0644\u0627\u0628\u064a',
                'verbose_name_plural': '\u0645\u0644\u0641\u0627\u062a \u0627\u0644\u0632\u0645\u0644\u0627\u0621 \u0627\u0644\u0637\u0644\u0627\u0628\u064a\u064a\u0646',
            },
            bases=('arshidni.arshidniprofile',),
        ),
        migrations.CreateModel(
            name='GraduateProfile',
            fields=[
                ('arshidniprofile_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='arshidni.ArshidniProfile')),
                ('bio', models.TextField(help_text='\u0645\u062a\u0649 \u062a\u062e\u0631\u062c\u062a\u061f \u0647\u0644 \u062e\u0636\u062a \u0623\u064a \u0627\u062e\u062a\u0628\u0627\u0631\u0627\u062a \u0639\u0627\u0644\u0645\u064a\u0629\u061f \u0647\u0644 \u0627\u0644\u062a\u062d\u0642\u062a \u0628\u0623\u064a \u0628\u0631\u0627\u0645\u062c\u061f', verbose_name='\u0646\u0628\u0630\u0629')),
                ('answers_questions', models.BooleanField(default=True, verbose_name='\u0647\u0644 \u062a\u0631\u064a\u062f \u0627\u0644\u0625\u062c\u0627\u0628\u0629 \u0639\u0644\u0649 \u0623\u0633\u0626\u0644\u0629 \u0627\u0644\u0637\u0644\u0627\u0628\u061f')),
                ('gives_lectures', models.BooleanField(default=True, verbose_name='\u0647\u0644 \u062a\u0631\u064a\u062f \u0625\u0644\u0642\u0627\u0621 \u0645\u062d\u0627\u0636\u0631\u0627\u062a \u0644\u0644\u0637\u0644\u0627\u0628 \u0639\u0646 \u0645\u0648\u0636\u0648\u0639 \u0645\u0646 \u0627\u062e\u062a\u064a\u0627\u0631\u0643\u061f')),
                ('user', models.OneToOneField(related_name='graduate_profile', null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0645\u0644\u0641 \u062e\u0631\u064a\u062c \u0645\u062a\u0639\u0627\u0648\u0646',
                'verbose_name_plural': '\u0645\u0644\u0641\u0627\u062a \u0627\u0644\u062e\u0631\u064a\u062c\u064a\u0646 \u0627\u0644\u0645\u062a\u0639\u0627\u0648\u0646\u064a\u0646',
            },
            bases=('arshidni.arshidniprofile',),
        ),
        migrations.CreateModel(
            name='JoinStudyGroupRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_accepted', models.NullBooleanField(default=None, verbose_name='\u0645\u0642\u0628\u0648\u0644\u061f', choices=[(None, '\u0644\u0645 \u062a\u0631\u0627\u062c\u0639 \u0628\u0639\u062f'), (True, '\u0645\u0642\u0628\u0648\u0644'), (False, '\u0645\u0631\u0641\u0648\u0636')])),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
            options={
                'verbose_name': '\u0637\u0644\u0628 \u0627\u0646\u0636\u0645\u0627\u0645 \u0644\u0645\u062c\u0645\u0648\u0639\u0629 \u062f\u0631\u0627\u0633\u064a\u0629',
                'verbose_name_plural': '\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0627\u0646\u0636\u0645\u0627\u0645 \u0644\u0645\u062c\u0645\u0648\u0639\u0629 \u062f\u0631\u0627\u0633\u064a\u0629',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LearningObjective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0648\u0635\u0641')),
                ('is_done', models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0623\u0646\u062c\u0632\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
            options={
                'verbose_name': '\u0647\u062f\u0641 \u062a\u0639\u0644\u064a\u0645\u064a',
                'verbose_name_plural': '\u0627\u0644\u0623\u0647\u062f\u0627\u0641 \u0627\u0644\u062a\u0639\u0644\u064a\u0645\u064a\u0629',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0646\u0635 \u0627\u0644\u0633\u0624\u0627\u0644')),
                ('college', models.CharField(max_length=1, verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629', choices=[(b'M', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0637\u0628'), (b'A', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0639\u0644\u0648\u0645 \u0627\u0644\u0637\u0628\u064a\u0629 \u0627\u0644\u062a\u0637\u0628\u064a\u0642\u064a\u0629'), (b'P', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0635\u064a\u062f\u0644\u0629'), (b'D', '\u0643\u0644\u064a\u0629 \u0637\u0628 \u0627\u0644\u0623\u0633\u0646\u0627\u0646'), (b'B', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0639\u0644\u0648\u0645 \u0648 \u0627\u0644\u0645\u0647\u0646 \u0627\u0644\u0635\u062d\u064a\u0629'), (b'N', '\u0643\u0644\u064a\u0629 \u0627\u0644\u062a\u0645\u0631\u064a\u0636'), (b'I', ' \u0643\u0644\u064a\u0629 \u0627\u0644\u0635\u062d\u0629 \u0627\u0644\u0639\u0627\u0645\u0629 \u0648\u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a\u064a\u0629 \u0627\u0644\u0635\u062d\u064a\u0629')])),
                ('is_published', models.NullBooleanField(default=True, verbose_name='\u0645\u0646\u0634\u0648\u0631\u061f', choices=[(None, '\u0644\u0645 \u064a\u0631\u0627\u062c\u0639 \u0628\u0639\u062f'), (True, '\u0645\u0646\u0634\u0648\u0631'), (False, '\u0645\u062d\u0630\u0648\u0641')])),
                ('is_answered', models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0623\u062c\u064a\u0628 \u0639\u0646\u0647\u061f')),
                ('is_editable', models.BooleanField(default=True, verbose_name='\u064a\u0645\u0643\u0646 \u062a\u0639\u062f\u064a\u0644\u0647\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0633\u0644', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u0633\u0624\u0627\u0644 \u0623\u0643\u0627\u062f\u064a\u0645\u064a',
                'verbose_name_plural': '\u0627\u0644\u0623\u0633\u0626\u0644\u0629 \u0627\u0644\u0623\u0643\u0627\u062f\u064a\u0645\u064a\u0629',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('starting_date', models.DateField(verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0628\u062f\u0621')),
                ('ending_date', models.DateField(verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0627\u0646\u062a\u0647\u0627\u0621')),
                ('max_members', models.PositiveSmallIntegerField(help_text='\u064a\u062c\u0628 \u0623\u0646 \u064a\u0643\u0648\u0646 \u0628\u064a\u0646 3 \u0648 8.', verbose_name='\u0627\u0644\u0639\u062f\u062f \u0627\u0644\u0623\u0642\u0635\u0649 \u0644\u0644\u0623\u0639\u0636\u0627\u0621')),
                ('is_published', models.NullBooleanField(default=True, verbose_name='\u0645\u0646\u0634\u0648\u0631\u061f', choices=[(None, '\u0644\u0645 \u064a\u0631\u0627\u062c\u0639 \u0628\u0639\u062f'), (True, '\u0645\u0646\u0634\u0648\u0631'), (False, '\u0645\u062d\u0630\u0648\u0641')])),
                ('status', models.CharField(default=b'P', max_length=1, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(b'P', '\u062a\u0646\u062a\u0638\u0631 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629'), (b'A', '\u0645\u0642\u0628\u0648\u0644\u0629'), (b'R', '\u0645\u0631\u0641\u0648\u0636\u0629')])),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('coordinator', models.ForeignKey(related_name='studygroup_coordination', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0646\u0633\u0642', to=settings.AUTH_USER_MODEL, null=True)),
                ('members', models.ManyToManyField(related_name='studygroup_memberships', null=True, verbose_name='\u0627\u0644\u0623\u0639\u0636\u0627\u0621', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': '\u0645\u062c\u0645\u0648\u0639\u0629 \u062f\u0631\u0627\u0633\u064a\u0629',
                'verbose_name_plural': '\u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0627\u062a \u0627\u0644\u062f\u0631\u0627\u0633\u064a\u0629',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SupervisionRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'P', max_length=2, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(b'P', '\u062a\u0646\u062a\u0638\u0631 \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629'), (b'A', '\u0645\u0642\u0628\u0648\u0644'), (b'R', '\u0645\u0631\u0641\u0648\u0636'), (b'D', '\u0623\u0644\u063a\u0627\u0647 \u0627\u0644\u0637\u0627\u0644\u0628 \u0627\u0644\u0645\u0633\u062a\u062c\u062f \u0642\u0628\u0644 \u0623\u0646 \u064a\u0631\u0627\u062c\u0639\u0647 \u0627\u0644\u0632\u0645\u064a\u0644 \u0627\u0644\u0637\u0644\u0627\u0628\u064a'), (b'WN', '\u0623\u0644\u063a\u0627\u0647 \u0627\u0644\u0637\u0627\u0644\u0628 \u0627\u0644\u0645\u0633\u062a\u062c\u062f'), (b'WC', '\u0623\u0644\u063a\u0627\u0647 \u0627\u0644\u0632\u0645\u064a\u0644 \u0627\u0644\u0637\u0644\u0627\u0628\u064a')])),
                ('contacts', models.CharField(help_text='\u062c\u0648\u0627\u0644 \u0645\u062b\u0644\u0627\u061f', max_length=100, verbose_name='\u0637\u0631\u064a\u0642\u0629 \u0627\u0644\u062a\u0648\u0627\u0635\u0644')),
                ('interests', models.TextField(help_text='\u0645\u0627 \u0627\u0644\u0645\u062c\u0627\u0644\u0627\u062a \u0627\u0644\u062a\u064a \u062a\u0631\u064a\u062f \u062a\u0637\u0648\u064a\u0631 \u0646\u0641\u0633\u0643 \u0641\u064a\u0647\u0627\u061f', verbose_name='\u0627\u0644\u0627\u0647\u062a\u0645\u0627\u0645\u0627\u062a')),
                ('batch', models.PositiveSmallIntegerField(verbose_name='\u0627\u0644\u062f\u0641\u0639\u0629')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('withdrawal_date', models.DateTimeField(default=None, null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0633\u062d\u0628')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('colleague', models.ForeignKey(related_name='colleague', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0632\u0645\u064a\u0644', to='arshidni.ColleagueProfile', null=True)),
                ('user', models.ForeignKey(related_name='supervision_requests', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0637\u0627\u0644\u0628 \u0627\u0644\u0645\u0633\u062a\u062c\u062f', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u0637\u0644\u0628 \u0632\u0645\u0627\u0644\u0629',
                'verbose_name_plural': '\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0632\u0645\u0627\u0644\u0629',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='learningobjective',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0629', to='arshidni.StudyGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joinstudygrouprequest',
            name='group',
            field=models.ForeignKey(related_name='join_requests', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0629', to='arshidni.StudyGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='joinstudygrouprequest',
            name='submitter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0633\u0644', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0633\u0644', to='arshidni.Question', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='submitter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0633\u0644', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
