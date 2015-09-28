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
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pages', models.PositiveSmallIntegerField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0635\u0641\u062d\u0627\u062a', blank=True)),
                ('title', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('authors', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0645\u0624\u0644\u0641')),
                ('edition', models.CharField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', max_length=200, verbose_name='\u0627\u0644\u0637\u0628\u0639\u0629', blank=True)),
                ('condition', models.CharField(help_text='\u0647\u0644 \u0645\u0646 \u0635\u0641\u062d\u0627\u062a \u0646\u0627\u0642\u0635\u0629 \u0623\u0648 \u0645\u0645\u0632\u0642\u0629 \u0645\u062b\u0644\u0627\u061f (\u0627\u062e\u062a\u064a\u0627\u0631\u064a)', max_length=2, verbose_name='\u062d\u0627\u0644\u0629 \u0627\u0644\u0643\u062a\u0627\u0628', choices=[(b'N', '\u0643\u0623\u0646\u0647 \u062c\u062f\u064a\u062f'), (b'VG', '\u062c\u064a\u062f\u0629 \u062c\u062f\u0627'), (b'G', '\u062c\u064a\u062f\u0629'), (b'P', '\u062f\u0648\u0646 \u0627\u0644\u062c\u064a\u062f\u0629')])),
                ('description', models.TextField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0643\u062a\u0627\u0628')),
                ('cover', models.FileField(upload_to=b'bulb/covers/', verbose_name='\u0627\u0644\u063a\u0644\u0627\u0641')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modifiation_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('is_available', models.BooleanField(default=True, verbose_name='\u0645\u062a\u0627\u062d\u061f')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u062a\u0635\u0646\u064a\u0641')),
                ('code_name', models.CharField(help_text='\u062d\u0631\u0648\u0641 \u0644\u0627\u062a\u064a\u0646\u064a\u0629 \u0635\u063a\u064a\u0631\u0629 \u0648\u0623\u0631\u0642\u0627\u0645', max_length=50, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u0628\u0631\u0645\u062c\u064a')),
                ('description', models.TextField(verbose_name='\u0648\u0635\u0641 \u0627\u0644\u062a\u0635\u0646\u064a\u0641', blank=True)),
                ('image', models.FileField(null=True, upload_to=b'bulb/categories/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('is_counted', models.BooleanField(default=True, verbose_name='\u0645\u062d\u0633\u0648\u0628\u0629\u061f')),
                ('note', models.CharField(default=b'', max_length=50, verbose_name='\u0645\u0644\u0627\u062d\u0638\u0629', blank=True)),
                ('value', models.IntegerField(verbose_name='\u0627\u0644\u0642\u064a\u0645\u0629')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('delivery', models.CharField(max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u062a\u0633\u0644\u064a\u0645', choices=[(b'D', '\u0625\u064a\u0635\u0627\u0644 \u0645\u0628\u0627\u0634\u0631'), (b'I', '\u0625\u064a\u0635\u0627\u0644 \u063a\u064a\u0631 \u0645\u0628\u0627\u0634\u0631')])),
                ('requester_status', models.CharField(default=b'', max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u062a\u0633\u0644\u064a\u0645', blank=True, choices=[(b'D', '\u062a\u0645'), (b'F', '\u062a\u0639\u0630\u0651\u0631'), (b'C', '\u0645\u0644\u063a\u0649')])),
                ('requester_status_date', models.DateTimeField(default=None, null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u062a\u0623\u0643\u064a\u062f \u0645\u0642\u062f\u0645 \u0627\u0644\u0637\u0644\u0628', blank=True)),
                ('owner_status', models.CharField(default=b'', max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u062a\u0633\u0644\u064a\u0645', blank=True, choices=[(b'D', '\u062a\u0645'), (b'F', '\u062a\u0639\u0630\u0651\u0631'), (b'C', '\u0645\u0644\u063a\u0649')])),
                ('owner_status_date', models.DateTimeField(default=None, null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u062a\u0623\u0643\u064a\u062f \u0635\u0627\u062d\u0628 \u0627\u0644\u0643\u062a\u0627\u0628', blank=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='bulb.Book', null=True)),
                ('requester', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='point',
            name='request',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0637\u0644\u0628', blank=True, to='bulb.Request', null=True),
        ),
        migrations.AddField(
            model_name='point',
            name='user',
            field=models.ForeignKey(related_name='book_points', verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='point',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0633\u0646\u0629', to='core.StudentClubYear', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641\u0627\u062a', to='bulb.Category', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='submitter',
            field=models.ForeignKey(related_name='book_giveaways', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.StudentClubYear', null=True),
        ),
    ]
