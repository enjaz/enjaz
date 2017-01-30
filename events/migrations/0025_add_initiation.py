# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0024_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Initiation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0645\u0628\u0627\u062f\u0631\u0629')),
                ('definition', models.TextField(verbose_name='\u062a\u0639\u0631\u064a\u0641 \u0627\u0644\u0645\u0628\u0627\u062f\u0631\u0629')),
                ('goals', models.TextField(verbose_name='\u0623\u0647\u062f\u0627\u0641 \u0627\u0644\u0645\u0628\u0627\u062f\u0631\u0629')),
                ('target', models.TextField(verbose_name='\u0627\u0644\u0641\u0626\u0629 \u0627\u0644\u0645\u0633\u062a\u0647\u062f\u0641\u0629')),
                ('achievements', models.TextField(verbose_name='\u0645\u0646\u062c\u0632\u0627\u062a \u0627\u0644\u0645\u0628\u0627\u062f\u0631\u0629 \u062d\u062a\u0649 \u0627\u0644\u0622\u0646')),
                ('future_goals', models.TextField(verbose_name='\u0645\u0627 \u0627\u0644\u0630\u064a \u062a\u062a\u0637\u0644\u0639 \u0627\u0644\u0645\u0628\u0627\u062f\u0631\u0629 \u0644\u0625\u0646\u062c\u0627\u0632\u0647 \u0645\u0633\u062a\u0642\u0628\u0644\u064b\u0627\u061f')),
                ('goals_from_participating', models.TextField(verbose_name='\u0645\u0627 \u0627\u0644\u0630\u064a \u062a\u0637\u0645\u062d \u0627\u0644\u0628\u0627\u062f\u0631\u0629 \u0644\u0644\u0648\u0635\u0648\u0644 \u0625\u0644\u064a\u0647 \u0645\u0646 \u062e\u0644\u0627\u0644 \u0627\u0644\u0645\u0624\u062a\u0645\u0631\u061f')),
                ('members', models.TextField(verbose_name='\u0645\u0646 \u0647\u0645 \u0627\u0644\u0642\u0627\u0626\u0645\u0648\u0646 \u0639\u0644\u0649 \u0627\u0644\u0639\u0645\u0644\u061f')),
                ('sponsors', models.TextField(help_text='\u0625\u0646 \u0648\u062c\u062f\u062a', verbose_name='\u0625\u0633\u0645 \u0627\u0644\u062c\u0647\u0629 \u0627\u0644\u0631\u0627\u0639\u064a\u0629', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a')),
                ('social', models.TextField(help_text='\u0625\u0646 \u0648\u062c\u062f\u062a', verbose_name='\u062d\u0633\u0627\u0628\u0627\u062a \u0627\u0644\u062a\u0648\u0627\u0635\u0644 \u0627\u0644\u0625\u062c\u062a\u0645\u0627\u0639\u064a \u0648\u0627\u0644\u0645\u0648\u0642\u0639 \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a', blank=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False, verbose_name='\u0645\u062d\u0630\u0648\u0641\u061f')),
            ],
        ),
        migrations.CreateModel(
            name='InitiationFigure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('figure', models.FileField(upload_to=b'events/figures/initiations/', verbose_name='Attach the figure')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='initiation_submission_closing_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0646\u062a\u0647\u0627\u0621 \u0625\u063a\u0644\u0627\u0642 \u0627\u0633\u062a\u0642\u0628\u0627\u0644 \u0627\u0644\u0645\u0628\u0627\u062f\u0631\u0627\u062a', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='initiation_submission_opening_date',
            field=models.DateTimeField(null=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0641\u062a\u062d \u0627\u0633\u062a\u0642\u0628\u0627\u0644 \u0627\u0644\u0645\u0628\u0627\u062f\u0631\u0627\u062a', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='receives_initiation_submission',
            field=models.BooleanField(default=False, verbose_name='\u064a\u0633\u062a\u0642\u0628\u0644 \u0645\u0628\u0627\u062f\u0631\u0627\u062a\u061f'),
        ),
        migrations.AddField(
            model_name='initiation',
            name='event',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u062d\u062f\u062b', to='events.Event'),
        ),
        migrations.AddField(
            model_name='initiation',
            name='user',
            field=models.ForeignKey(related_name='initiator', to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
