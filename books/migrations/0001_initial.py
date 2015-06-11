# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isbn', models.CharField(help_text='\u0645\u0637\u0644\u0648\u0628', max_length=13, verbose_name='\u0631\u062f\u0645\u0643')),
                ('pages', models.PositiveSmallIntegerField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', null=True, verbose_name='\u0639\u062f\u062f \u0627\u0644\u0635\u0641\u062d\u0627\u062a', blank=True)),
                ('title', models.CharField(help_text='\u0645\u0637\u0644\u0648\u0628', max_length=200, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('authors', models.CharField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', max_length=200, verbose_name='\u062a\u0623\u0644\u064a\u0641', blank=True)),
                ('publisher', models.CharField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', max_length=200, verbose_name='\u0627\u0644\u0646\u0627\u0634\u0631', blank=True)),
                ('year', models.PositiveSmallIntegerField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', null=True, verbose_name='\u0633\u0646\u0629 \u0627\u0644\u0646\u0634\u0631', blank=True)),
                ('edition', models.CharField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', max_length=200, verbose_name='\u0627\u0644\u0637\u0628\u0639\u0629', blank=True)),
                ('condition', models.CharField(blank=True, help_text='\u0647\u0644 \u0645\u0646 \u0635\u0641\u062d\u0627\u062a \u0646\u0627\u0642\u0635\u0629 \u0623\u0648 \u0645\u0645\u0632\u0642\u0629 \u0645\u062b\u0644\u0627\u061f (\u0627\u062e\u062a\u064a\u0627\u0631\u064a)', max_length=200, verbose_name='\u062d\u0627\u0644\u0629 \u0627\u0644\u0643\u062a\u0627\u0628', choices=[(b'Like new', '\u0643\u0623\u0646\u0647 \u062c\u062f\u064a\u062f'), (b'Very good', '\u062c\u064a\u062f\u0629 \u062c\u062f\u0627'), (b'Good', '\u062c\u064a\u062f\u0629'), (b'Poor', '\u062f\u0648\u0646 \u0627\u0644\u062c\u064a\u062f\u0629')])),
                ('description', models.TextField(help_text='\u0627\u062e\u062a\u064a\u0627\u0631\u064a', verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0643\u062a\u0627\u0628', blank=True)),
                ('contact', models.CharField(help_text='\u0631\u0642\u0645 \u062c\u0648\u0627\u0644 \u0623\u0648 \u0639\u0646\u0648\u0627\u0646 \u0628\u0631\u064a\u062f (\u0645\u0637\u0644\u0648\u0628)', max_length=200, verbose_name='\u0637\u0631\u064a\u0642\u0629 \u0627\u0644\u062a\u0648\u0627\u0635\u0644')),
                ('status', models.CharField(default=b'A', max_length=1, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(b'A', '\u0645\u062a\u0627\u062d'), (b'H', '\u0645\u062d\u062c\u0648\u0632'), (b'B', '\u0645\u0639\u0627\u0631'), (b'W', '\u0645\u0633\u062d\u0648\u0628'), (b'R', '\u0645\u0639\u0627\u062f')])),
                ('available_to', models.CharField(max_length=1, verbose_name='\u0645\u062a\u0627\u062d \u0644\u0642\u0633\u0645', choices=[(b'M', '\u0627\u0644\u0637\u0644\u0627\u0628'), (b'F', '\u0627\u0644\u0637\u0627\u0644\u0628\u0627\u062a')])),
                ('cover_url', models.CharField(help_text='\u0635\u0648\u0631\u0629 \u0644\u063a\u0644\u0627\u0641 \u0627\u0644\u0643\u062a\u0627\u0628 (\u0645\u0633\u062a\u062d\u0633\u0646)', max_length=200, verbose_name='\u0635\u0648\u0631\u0629 \u0627\u0644\u063a\u0644\u0627\u0641', blank=True)),
                ('cover', models.FileField(null=True, upload_to=b'covers', blank=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modifiation_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('available_from', models.DateField(help_text='\u062a\u0631\u063a\u0628 \u0641\u064a \u0625\u0639\u0627\u0631\u0629 \u0647\u0630\u0627 \u0627\u0644\u0643\u062a\u0627\u0628 \u0627\u0628\u062a\u062f\u0627\u0621\u064b \u0645\u0646 \u0647\u0630\u0627 \u0627\u0644\u062a\u0627\u0631\u064a\u062e (\u0645\u0637\u0644\u0648\u0628)', verbose_name='\u0645\u062a\u0648\u0641\u0631 \u0627\u0628\u062a\u062f\u0627\u0621\u064b \u0645\u0646')),
                ('available_until', models.DateField(help_text='\u062a\u0631\u063a\u0628 \u0641\u064a \u0625\u0639\u0627\u0631\u0629 \u0647\u0630\u0627 \u0627\u0644\u0643\u062a\u0627\u0628 \u062d\u062a\u0649 \u0647\u0630\u0627 \u0627\u0644\u062a\u0627\u0631\u064a\u062e (\u0627\u062e\u062a\u064a\u0627\u0631\u064a)', null=True, verbose_name='\u0645\u062a\u0648\u0641\u0631 \u062d\u062a\u0649', blank=True)),
                ('holder', models.ForeignKey(related_name='book_holdings', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('submitter', models.ForeignKey(related_name='book_contributions', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='\u0645\u0627 \u0627\u0644\u062a\u0635\u0627\u0646\u064a\u0641 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629 \u0627\u0644\u062a\u064a \u062a\u0631\u0627\u0647\u0627 \u0645\u0644\u0627\u0626\u0645\u0629\u061f (\u0645\u0637\u0644\u0648\u0628\u0629 \u0648\u0645\u0641\u0635\u0648\u0644\u0629 \u0628\u0641\u0648\u0627\u0635\u0644\u060c \u0645\u062b\u0644\u0627: "Respiratory, Physiology")', verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641\u0627\u062a')),
            ],
            options={
                'permissions': (('view_books', 'Can see all books regardless of their status.'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BookRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'P', max_length=1, verbose_name='\u0627\u0644\u062d\u0627\u0644\u0629', choices=[(b'P', '\u0645\u0639\u0644\u0642\u0629'), (b'W', '\u0645\u0644\u063a\u0627\u0629'), (b'A', '\u0645\u0642\u0628\u0648\u0644\u0629'), (b'R', '\u0645\u0631\u0641\u0648\u0636\u0629'), (b'S', '\u0623\u0639\u064a\u062f \u0627\u0644\u0643\u062a\u0627\u0628')])),
                ('borrow_from', models.DateField(verbose_name='\u0627\u0633\u062a\u0639\u0631 \u0645\u0646')),
                ('borrow_until', models.DateField(verbose_name='\u0627\u0633\u062a\u0639\u0631 \u062d\u062a\u0649')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modifiation_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='books.Book', null=True)),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
