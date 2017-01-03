# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulb', '0027_readathon_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReadathonFiles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(upload_to=b'readathon/attachment/', verbose_name='\u0645\u0644\u0641')),
            ],
        ),
        migrations.CreateModel(
            name='ReadathonProducts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=200, verbose_name='\u0623\u0633\u0645 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640\\\u0640\u0629')),
                ('title', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('body', models.TextField(default=False)),
                ('readathon', models.ForeignKey(to='bulb.Readathon', to_field='\u0627\u0644\u0631\u064a\u062f\u064a\u062b\u0648\u0646')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629')),
            ],
        ),
        migrations.RemoveField(
            model_name='culturalproduct',
            name='readathon',
        ),
        migrations.RemoveField(
            model_name='debate',
            name='invitation',
        ),
        migrations.RemoveField(
            model_name='debatecomment',
            name='debate',
        ),
        migrations.RemoveField(
            model_name='debatecomment',
            name='user',
        ),
        migrations.DeleteModel(
            name='CulturalProduct',
        ),
        migrations.DeleteModel(
            name='Debate',
        ),
        migrations.DeleteModel(
            name='DebateComment',
        ),
        migrations.AddField(
            model_name='readathonfiles',
            name='readathon_products',
            field=models.ForeignKey(related_name='attachment', to='bulb.ReadathonProducts'),
        ),
    ]
