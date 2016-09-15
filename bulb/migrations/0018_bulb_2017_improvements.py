# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import tagging_autocomplete.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0007_tweet'),
        ('bulb', '0017_add_2017_bulb_clubs'),
    ]

    operations = [
        migrations.CreateModel(
            name='NeededBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tags', tagging_autocomplete.models.TagAutocompleteField(max_length=255, verbose_name='\u0627\u0644\u0648\u0633\u0648\u0645', blank=True)),
                ('title', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('cover', models.ImageField(upload_to=b'bulb/covers/', verbose_name='\u0627\u0644\u063a\u0644\u0627\u0641')),
                ('authors', models.CharField(max_length=200, verbose_name='\u062a\u0623\u0644\u064a\u0641')),
                ('description', models.TextField(verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0643\u062a\u0627\u0628')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
            ],
        ),
        migrations.RemoveField(
            model_name='group',
            name='gender',
        ),
        migrations.AddField(
            model_name='book',
            name='is_publicly_owned',
            field=models.BooleanField(default=False, verbose_name='\u0643\u062a\u0627\u0628 \u0639\u0645\u0648\u0645\u064a \u0644\u0627 \u064a\u064f\u0646\u0633\u0628 \u0644\u062d\u0633\u0627\u0628 \u0628\u0639\u064a\u0646\u0647.'),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=tagging_autocomplete.models.TagAutocompleteField(max_length=255, verbose_name='\u0627\u0644\u0648\u0633\u0648\u0645', blank=True),
        ),
        migrations.AddField(
            model_name='group',
            name='is_archived',
            field=models.BooleanField(default=False, verbose_name='\u0645\u0624\u0631\u0634\u0641\u0629\u061f'),
        ),
        migrations.AddField(
            model_name='group',
            name='is_limited_by_city',
            field=models.BooleanField(default=True, verbose_name='\u0645\u062d\u062f\u0648\u062f\u0629 \u0628\u0627\u0644\u0645\u062f\u064a\u0646\u0629'),
        ),
        migrations.AddField(
            model_name='group',
            name='is_limited_by_gender',
            field=models.BooleanField(default=True, verbose_name='\u0645\u062d\u062f\u0648\u062f\u0629 \u0628\u0627\u0644\u062c\u0646\u062f\u0631'),
        ),
        migrations.AddField(
            model_name='group',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0644\u0645\u062c\u0645\u0648\u0639\u0629 \u062e\u0627\u0635\u0629 \u0648\u062a\u0637\u0644\u0628 \u0645\u0648\u0627\u0641\u0642\u0629 \u0642\u0628\u0644 \u0627\u0644\u0646\u0636\u0645\u0627\u0645 \u0648\u0627\u0644\u0627\u0637\u0644\u0627\u0639\u061f'),
        ),
        migrations.AddField(
            model_name='session',
            name='confirmed_attendees',
            field=models.ManyToManyField(related_name='sessions_confirmed', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='session',
            name='is_limited_by_city',
            field=models.BooleanField(default=True, verbose_name='\u0645\u062d\u062f\u0648\u062f\u0629 \u0628\u0627\u0644\u0645\u062f\u064a\u0646\u0629'),
        ),
        migrations.AddField(
            model_name='session',
            name='is_limited_by_gender',
            field=models.BooleanField(default=True, verbose_name='\u0645\u062d\u062f\u0648\u062f\u0629 \u0628\u0627\u0644\u062c\u0646\u062f\u0631'),
        ),
        migrations.AddField(
            model_name='session',
            name='submitter',
            field=models.ForeignKey(related_name='sessions_submitted', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.StudentClubYear', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='authors',
            field=models.CharField(max_length=200, verbose_name='\u062a\u0623\u0644\u064a\u0641'),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0642\u0633\u0645', to='bulb.Category', null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='cover',
            field=models.ImageField(upload_to=b'bulb/covers/', verbose_name='\u0627\u0644\u063a\u0644\u0627\u0641'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to=b'bulb/categories/', blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='image',
            field=models.ImageField(upload_to=b'bulb/groups/', verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629'),
        ),
        migrations.AddField(
            model_name='neededbook',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0642\u0633\u0645', to='bulb.Category', null=True),
        ),
        migrations.AddField(
            model_name='neededbook',
            name='existing_book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='bulb.Book', null=True),
        ),
        migrations.AddField(
            model_name='neededbook',
            name='requester',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='neededbook',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.StudentClubYear', null=True),
        ),
    ]
