# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_years'),
        ('clubs', '0022_club_can_review_niqati'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('niqati', '0002_add_categories'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_reviewed', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0645\u0631\u0627\u062c\u0639\u0629', null=True)),
                ('is_approved', models.NullBooleanField(default=None)),
            ],
        ),
        migrations.DeleteModel(
            name='Niqati_User',
        ),
        migrations.RemoveField(
            model_name='category',
            name='requires_approval',
        ),
        migrations.RemoveField(
            model_name='code',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='code_collection',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='code_collection',
            name='date_ordered',
        ),
        migrations.RemoveField(
            model_name='code_collection',
            name='delivery_type',
        ),
        migrations.AddField(
            model_name='code',
            name='note',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AddField(
            model_name='code',
            name='points',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='code',
            name='short_link',
            field=models.URLField(null=True, verbose_name='\u0631\u0627\u0628\u0637 \u0642\u0635\u064a\u0631', blank=True),
        ),
        migrations.AddField(
            model_name='code',
            name='year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='core.StudentClubYear', null=True),
        ),
        migrations.AddField(
            model_name='code_collection',
            name='date_downloaded',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0646\u0632\u064a\u0644', blank=True),
        ),
        migrations.AddField(
            model_name='code_order',
            name='assignee',
            field=models.ForeignKey(related_name='assigned_niqati_orders', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0645\u0633\u0646\u062f', blank=True, to='clubs.Club', null=True),
        ),
        migrations.AddField(
            model_name='code_order',
            name='submitter',
            field=models.ForeignKey(related_name='submitted_code', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='points',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name='code',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='niqati.Code_Collection', null=True),
        ),
        migrations.AlterField(
            model_name='code',
            name='redeem_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u062f\u062e\u0627\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='code_collection',
            name='code_count',
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AddField(
            model_name='review',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='niqati.Code_Order', null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(related_name='reviewed_niqati_orders', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='review',
            name='reviewer_club',
            field=models.ForeignKey(related_name='reviewed_niqati_orders', verbose_name='\u0627\u0644\u0646\u0627\u062f\u064a \u0627\u0644\u0645\u0631\u0627\u062c\u0650\u0639', to='clubs.Club', null=True),
        ),
    ]
