# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=20)),
                ('ar_label', models.CharField(max_length=20)),
                ('points', models.IntegerField()),
                ('requires_approval', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code_string', models.CharField(unique=True, max_length=16)),
                ('generation_date', models.DateTimeField(auto_now_add=True)),
                ('asset', models.CharField(max_length=300, blank=True)),
                ('redeem_date', models.DateTimeField(null=True, blank=True)),
                ('category', models.ForeignKey(to='niqati.Category')),
            ],
            options={
                'verbose_name': '\u0646\u0642\u0637\u0629',
                'verbose_name_plural': '\u0627\u0644\u0646\u0642\u0627\u0637',
                'permissions': (('submit_code', 'Can submit a code.'), ('view_student_report', "Can view a report of own's codes."), ('view_general_report', 'Can view a report of all students.')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Code_Collection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('code_count', models.IntegerField()),
                ('approved', models.NullBooleanField(default=None)),
                ('delivery_type', models.CharField(max_length=1, choices=[(b'0', '\u0643\u0648\u0628\u0648\u0646\u0627\u062a'), (b'1', '\u0631\u0648\u0627\u0628\u0637 \u0642\u0635\u064a\u0631\u0629')])),
                ('date_created', models.DateTimeField(default=None, null=True, blank=True)),
                ('asset', models.FileField(upload_to=b'niqati/codes/')),
                ('code_category', models.ForeignKey(to='niqati.Category')),
            ],
            options={
                'verbose_name': '\u0645\u062c\u0645\u0648\u0639\u0629 \u0646\u0642\u0627\u0637',
                'verbose_name_plural': '\u0645\u062c\u0645\u0648\u0639\u0627\u062a \u0627\u0644\u0646\u0642\u0627\u0637',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Code_Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('episode', models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0648\u0639\u062f', to='activities.Episode')),
            ],
            options={
                'verbose_name': '\u0637\u0644\u0628 \u0646\u0642\u0627\u0637',
                'verbose_name_plural': '\u0637\u0644\u0628\u0627\u062a \u0627\u0644\u0646\u0642\u0627\u0637',
                'permissions': (('request_order', 'Can place a request for a code order.'), ('view_order', 'Can view existing code orders.'), ('approve_order', 'Can approve order requests.')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='code_collection',
            name='parent_order',
            field=models.ForeignKey(to='niqati.Code_Order'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='code',
            name='collection',
            field=models.ForeignKey(to='niqati.Code_Collection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='code',
            name='episode',
            field=models.ForeignKey(to='activities.Episode'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='code',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Niqati_User',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
        ),
    ]
