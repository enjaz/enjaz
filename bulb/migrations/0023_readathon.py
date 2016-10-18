# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulb', '0022_dewanyasuggestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookCommitment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
                ('cover', models.ImageField(upload_to=b'bulb/book_commitments/', verbose_name='\u0627\u0644\u063a\u0644\u0627\u0641')),
                ('reason', models.TextField(help_text='\u0628\u0646\u0627\u0621 \u0639\u0644\u0649 \u0647\u0630\u0647 \u0627\u0644\u0625\u062c\u0627\u0628\u0629\u060c \u0633\u064a\u0643\u0648\u0646 \u0627\u0644\u0627\u062e\u062a\u064a\u0627\u0631 \u0644\u062c\u0644\u0633\u0629 \u0627\u0644\u0646\u0642\u0627\u0634 \u0627\u0644\u0645\u0635\u063a\u0631\u0629.', verbose_name='\u0644\u0645\u0627\u0630\u0627 \u062a\u0648\u062f\u0651/\u064a\u0646 \u0642\u0631\u0627\u0621\u0629 \u0647\u0630\u0627 \u0627\u0644\u0643\u062a\u0627\u0628 \u0641\u064a \u0627\u0644\u0631\u064a\u062f\u064a\u062b\u0648\u0646\u061f', blank=True)),
                ('wants_to_attend', models.BooleanField(default=False, verbose_name='\u062a\u0648\u062f/\u064a\u0646 \u062d\u0636\u0648\u0631 \u062c\u0644\u0633\u0629 \u0627\u0644\u0646\u0642\u0627\u0634 \u0627\u0644\u0645\u0635\u063a\u0631\u0629\u061f')),
                ('wants_to_contribute', models.BooleanField(default=False, verbose_name='\u062a\u0648\u062f/\u064a\u0646 \u0627\u0644\u0645\u0633\u0627\u0647\u0645\u0629 \u0628\u0645\u0646\u062a\u062c \u062b\u0642\u0627\u0641\u064a \u0628\u0639\u062f \u0625\u062a\u0645\u0627\u0645 \u062e\u0637\u0651\u0629 \u0627\u0644\u0642\u0631\u0627\u0621\u0629\u061f')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0647\u0644 \u062d\u064f\u0630\u0641\u061f')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
            ],
        ),
        migrations.CreateModel(
            name='Readathon',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publication_date', models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0646\u0634\u0631', blank=True)),
                ('start_date', models.DateField(verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0628\u062f\u0627\u064a\u0629')),
                ('end_date', models.DateField(verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0646\u0647\u0627\u064a\u0629')),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('template_name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0639\u0646\u0648\u0627\u0646')),
            ],
        ),
        migrations.AddField(
            model_name='bookcommitment',
            name='readathon',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0631\u064a\u062f\u064a\u062b\u0648\u0646', to='bulb.Readathon'),
        ),
        migrations.AddField(
            model_name='bookcommitment',
            name='user',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', to=settings.AUTH_USER_MODEL),
        ),
    ]
