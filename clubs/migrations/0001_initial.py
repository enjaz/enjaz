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
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('english_name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a')),
                ('description', models.TextField(verbose_name='\u0627\u0644\u0648\u0635\u0641')),
                ('email', models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0646\u0634\u0627\u0621')),
                ('edit_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('special', models.BooleanField(default=False, verbose_name='\u0646\u0627\u062f\u064a \u0645\u0645\u064a\u0632\u061f')),
                ('city', models.CharField(max_length=1, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', choices=[(b'R', '\u0627\u0644\u0631\u064a\u0627\u0636'), (b'J', '\u062c\u062f\u0629'), (b'A', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')])),
            ],
            options={
                'verbose_name': '\u0646\u0627\u062f\u064a',
                'verbose_name_plural': '\u0627\u0644\u0623\u0646\u062f\u064a\u0629',
                'permissions': (('view_members', 'Can view club members list.'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('section', models.CharField(max_length=2, verbose_name='\u0627\u0644\u0642\u0633\u0645', choices=[(b'NG', '\u0627\u0644\u062d\u0631\u0633 \u0627\u0644\u0648\u0637\u0646\u064a'), (b'KF', '\u0645\u062f\u064a\u0646\u0629 \u0627\u0644\u0645\u0644\u0643 \u0641\u0647\u062f \u0627\u0644\u0637\u0628\u064a\u0629')])),
                ('name', models.CharField(max_length=1, verbose_name='\u0627\u0644\u0627\u0633\u0645', choices=[(b'M', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0637\u0628'), (b'A', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0639\u0644\u0648\u0645 \u0627\u0644\u0637\u0628\u064a\u0629 \u0627\u0644\u062a\u0637\u0628\u064a\u0642\u064a\u0629'), (b'P', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0635\u064a\u062f\u0644\u0629'), (b'D', '\u0643\u0644\u064a\u0629 \u0637\u0628 \u0627\u0644\u0623\u0633\u0646\u0627\u0646'), (b'B', '\u0643\u0644\u064a\u0629 \u0627\u0644\u0639\u0644\u0648\u0645 \u0648 \u0627\u0644\u0645\u0647\u0646 \u0627\u0644\u0635\u062d\u064a\u0629'), (b'N', '\u0643\u0644\u064a\u0629 \u0627\u0644\u062a\u0645\u0631\u064a\u0636'), (b'I', ' \u0643\u0644\u064a\u0629 \u0627\u0644\u0635\u062d\u0629 \u0627\u0644\u0639\u0627\u0645\u0629 \u0648\u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a\u064a\u0629 \u0627\u0644\u0635\u062d\u064a\u0629')])),
                ('city', models.CharField(max_length=1, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', choices=[(b'R', '\u0627\u0644\u0631\u064a\u0627\u0636'), (b'J', '\u062c\u062f\u0629'), (b'A', '\u0627\u0644\u0623\u062d\u0633\u0627\u0621')])),
                ('gender', models.CharField(max_length=1, verbose_name='\u0627\u0644\u062c\u0646\u0633', choices=[(b'F', '\u0637\u0627\u0644\u0628\u0627\u062a'), (b'M', '\u0637\u0644\u0627\u0628')])),
            ],
            options={
                'verbose_name': '\u0643\u0644\u064a\u0629',
                'verbose_name_plural': '\u0627\u0644\u0643\u0644\u064a\u0627\u062a',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='club',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='clubs.College', null=True, verbose_name='\u0627\u0644\u0643\u0644\u064a\u0629'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='coordinator',
            field=models.ForeignKey(related_name='coordination', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0645\u0646\u0633\u0642', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='deputies',
            field=models.ManyToManyField(related_name='deputyships', null=True, verbose_name='\u0627\u0644\u0646\u0648\u0627\u0628', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='employee',
            field=models.ForeignKey(related_name='employee', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='\u0627\u0644\u0645\u0648\u0638\u0641 \u0627\u0644\u0645\u0633\u0624\u0648\u0644'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(related_name='memberships', null=True, verbose_name='\u0627\u0644\u0623\u0639\u0636\u0627\u0621', to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='club',
            name='parent',
            field=models.ForeignKey(related_name='parenthood', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='clubs.Club', null=True, verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0623\u0628'),
            preserve_default=True,
        ),
    ]
