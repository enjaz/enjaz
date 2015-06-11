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
            name='Recipient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('english_name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a')),
                ('email', models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a')),
                ('secondary_email', models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('college', models.ManyToManyField(to='clubs.College', null=True, verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629', blank=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0648\u0646', blank=True)),
            ],
            options={
                'verbose_name': '\u0645\u0633\u062a\u0642\u0628\u0644',
                'verbose_name_plural': '\u0627\u0644\u0645\u0633\u062a\u0642\u0628\u0644\u0648\u0646',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0646\u0635')),
                ('is_published', models.BooleanField(default=True, verbose_name='\u0645\u0646\u0634\u0648\u0631\u061f')),
                ('is_editable', models.BooleanField(default=True, verbose_name='\u064a\u0645\u0643\u0646 \u062a\u0639\u062f\u064a\u0644\u0647\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u062c\u064a\u0628', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u0627\u0633\u062a\u062c\u0627\u0628\u0629',
                'verbose_name_plural': '\u0627\u0644\u0627\u0633\u062a\u062c\u0627\u0628\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_counted', models.BooleanField(default=True, verbose_name='\u0645\u062d\u0633\u0648\u0628\u0629\u061f')),
                ('view_date', models.DateTimeField(auto_now_add=True, verbose_name=b'date viewed')),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0634\u0627\u0647\u062f', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u0645\u0634\u0627\u0647\u062f\u0629',
                'verbose_name_plural': '\u0627\u0644\u0645\u0634\u0627\u0647\u062f\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Voice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='\u0644\u062e\u0635 \u0635\u0648\u062a\u0643 \u0641\u064a \u0639\u0634\u0631 \u0643\u0644\u0645\u0627\u062a \u0623\u0648 \u0623\u0642\u0644', max_length=100, verbose_name='\u0645\u0644\u062e\u0635', blank=True)),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0646\u0635')),
                ('solution', models.TextField(verbose_name='\u0627\u0644\u062d\u0644 \u0627\u0644\u0645\u0642\u062a\u0631\u062d', blank=True)),
                ('was_sent', models.BooleanField(default=False, verbose_name='\u0623\u0631\u0633\u0644\u061f')),
                ('is_published', models.NullBooleanField(default=True, verbose_name='\u0645\u0646\u0634\u0648\u0631\u061f', choices=[(None, '\u0644\u0645 \u064a\u0631\u0627\u062c\u0639 \u0628\u0639\u062f'), (True, '\u0645\u0646\u0634\u0648\u0631'), (False, '\u0645\u062d\u0630\u0648\u0641')])),
                ('is_editable', models.BooleanField(default=True, verbose_name='\u064a\u0645\u0643\u0646 \u062a\u0639\u062f\u064a\u0644\u0647\u061f')),
                ('score', models.IntegerField(default=0, verbose_name='\u0627\u0644\u062f\u0631\u062c\u0629')),
                ('number_of_views', models.IntegerField(default=0, verbose_name='\u0627\u0644\u0645\u0634\u0627\u0647\u062f\u0627\u062a')),
                ('number_of_comments', models.IntegerField(default=0, verbose_name='\u0627\u0644\u062a\u0639\u0644\u064a\u0642\u0627\u062a')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0646\u0634\u0631')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('parent', models.ForeignKey(related_name='replies', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0631\u062f \u0639\u0644\u0649', blank=True, to='studentvoice.Voice', null=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u0642\u0628\u0644', blank=True, to='studentvoice.Recipient', null=True)),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0631\u0633\u0644', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u0635\u0648\u062a',
                'verbose_name_plural': '\u0627\u0644\u0623\u0635\u0648\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_counted', models.BooleanField(default=True, verbose_name='\u0645\u062d\u0633\u0648\u0628\u061f')),
                ('vote_type', models.CharField(max_length=1, choices=[(b'U', '\u0645\u0639'), (b'D', '\u0636\u062f'), (b'R', '\u0628\u0644\u0627\u063a')])),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('submitter', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0635\u0648\u062a', to=settings.AUTH_USER_MODEL, null=True)),
                ('voice', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0635\u0648\u062a', to='studentvoice.Voice', null=True)),
            ],
            options={
                'verbose_name': '\u0627\u0642\u062a\u0631\u0627\u0639',
                'verbose_name_plural': '\u0627\u0644\u0627\u0642\u062a\u0631\u0627\u0639\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='view',
            name='voice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0635\u0648\u062a', to='studentvoice.Voice', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response',
            name='voice',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0635\u0648\u062a', to='studentvoice.Voice'),
            preserve_default=True,
        ),
    ]
