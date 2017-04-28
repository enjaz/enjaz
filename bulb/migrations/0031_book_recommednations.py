# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulb', '0030_auto_20170303_2039'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookRecommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(verbose_name='\u062a\u0639\u0644\u064a\u0642')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0647\u0644 \u062d\u064f\u0630\u0641\u061f')),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
            ],
        ),
        migrations.CreateModel(
            name='RecommendedBook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'\xd8\xa7\xd9\x84\xd8\xb9\xd9\x86\xd9\x88\xd8\xa7\xd9\x86')),
                ('authors', models.CharField(max_length=200, verbose_name='\u062a\u0623\u0644\u064a\u0641')),
                ('cover', models.ImageField(upload_to=b'bulb/covers/', verbose_name='\u0627\u0644\u063a\u0644\u0627\u0641')),
                ('date_submitted', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('category', models.ForeignKey(verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641', to='bulb.Category')),
            ],
        ),
        migrations.AddField(
            model_name='bookrecommendation',
            name='recommended_book',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0643\u062a\u0627\u0628 \u0627\u0644\u0645\u0648\u0635\u0649', to='bulb.RecommendedBook'),
        ),
        migrations.AddField(
            model_name='bookrecommendation',
            name='user',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', to=settings.AUTH_USER_MODEL),
        ),
    ]
