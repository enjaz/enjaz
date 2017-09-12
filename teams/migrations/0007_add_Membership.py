# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teams', '0006_add_is_open'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accepted', models.BooleanField(default=False)),
                ('registration_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0633\u062c\u064a\u0644')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644', null=True)),
                ('member', models.ForeignKey(verbose_name='\u0627\u0644\u0639\u0636\u0648', to=settings.AUTH_USER_MODEL)),
                ('team', models.ForeignKey(verbose_name='\u0627\u0644\u0641\u0631\u064a\u0642', to='teams.Team')),
            ],
            options={
                'verbose_name': '\u0627\u0644\u0639\u0636\u0648\u064a\u0629',
                'verbose_name_plural': '\u0627\u0644\u0639\u0636\u0648\u064a\u0627\u062a',
            },
        ),
        migrations.AddField(
            model_name='team',
            name='members2',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u0627\u0644\u0623\u0639\u0636\u0627\u0621', through='teams.Membership', blank=True),
        ),
    ]
