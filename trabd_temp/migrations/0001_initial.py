# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Nomination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('plan', models.FileField(upload_to=b'', verbose_name=b'\xd8\xa7\xd9\x84\xd8\xae\xd8\xb7\xd8\xa9')),
                ('cv', models.FileField(upload_to=b'', verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb3\xd9\x8a\xd8\xb1\xd8\xa9 \xd8\xa7\xd9\x84\xd8\xb0\xd8\xa7\xd8\xaa\xd9\x8a\xd8\xa9')),
                ('certificates', models.FileField(upload_to=b'', null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb4\xd9\x87\xd8\xa7\xd8\xaf\xd8\xa7\xd8\xaa \xd9\x88\xd8\xa7\xd9\x84\xd9\x85\xd8\xb3\xd8\xa7\xd9\x87\xd9\x85\xd8\xa7\xd8\xaa')),
                ('gpa', models.FloatField(null=True, verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb9\xd8\xaf\xd9\x84 \xd8\xa7\xd9\x84\xd8\xac\xd8\xa7\xd9\x85\xd8\xb9\xd9\x8a')),
                ('position', models.TextField(verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd9\x86\xd8\xb5\xd8\xa8')),
                ('city', models.CharField(default=b'', max_length=1, verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xaf\xd9\x8a\xd9\x86\xd8\xa9', blank=True, choices=[(b'', b'\xd8\xb9\xd8\xa7\xd9\x85\xd8\xa9'), (b'R', b'\xd8\xa7\xd9\x84\xd8\xb1\xd9\x8a\xd8\xa7\xd8\xb6'), (b'J', b'\xd8\xac\xd8\xaf\xd8\xa9'), (b'A', b'\xd8\xa7\xd9\x84\xd8\xa3\xd8\xad\xd8\xb3\xd8\xa7\xd8\xa1')])),
                ('is_rejected', models.BooleanField(default=False)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name=b'\xd8\xaa\xd8\xa7\xd8\xb1\xd9\x8a\xd8\xae \xd8\xa7\xd9\x84\xd8\xaa\xd9\x82\xd8\xaf\xd9\x8a\xd9\x85')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name=b'\xd8\xaa\xd8\xa7\xd8\xb1\xd9\x8a\xd8\xae \xd8\xa7\xd9\x84\xd8\xaa\xd8\xb9\xd8\xaf\xd9\x8a\xd9\x84', null=True)),
                ('user', models.ForeignKey(verbose_name=b'\xd8\xa7\xd9\x84\xd9\x85\xd8\xb1\xd8\xb4\xd9\x91\xd9\x8e\xd8\xad', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0627\u0644\u0645\u0631\u0634\u062d\u0640/\u0640\u0629',
                'verbose_name_plural': '\u0627\u0644\u0645\u0631\u0634\u062d\u0648\u0646/\u0627\u0644\u0645\u0631\u0634\u0651\u062d\u0627\u062a',
            },
        ),
    ]
