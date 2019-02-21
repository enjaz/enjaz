# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tedx', '0004_game'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='id_code',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='registration',
            name='about_tedx',
            field=models.TextField(null=True, verbose_name='\u062a\u062d\u062f\u062b \u0639\u0646 \u062a\u062f\u0643\u0633', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='age',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='\u0639\u0645\u0631\u0643', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='attend_tedx',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0633\u0628\u0642 \u0648\u062d\u0636\u0631\u062a \u062a\u062f\u0643\u0633\u061f'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='city',
            field=models.CharField(max_length=10, null=True, verbose_name='\u0627\u0644\u0645\u062f\u064a\u0646\u0629', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='emial',
            field=models.EmailField(max_length=100, null=True, verbose_name='\u0627\u0644\u0628\u0631\u064a\u062f \u0627\u0644\u0625\u0644\u0643\u062a\u0631\u0648\u0646\u064a', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='expectations',
            field=models.TextField(null=True, verbose_name='\u0645\u0627\u0630\u0627 \u062a\u062a\u0648\u0642\u0639 \u0623\u0646 \u062a\u0633\u062a\u0641\u064a\u062f \u0645\u0646 TEDxKSAUHS?', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='fromNGH',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0623\u0646\u062a \u0645\u0646 \u0645\u0646\u0633\u0648\u0628\u064a \u0648\u0645\u0646\u0633\u0648\u0628\u0627\u062a \u0627\u0644\u062d\u0631\u0633\u061f'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='gender',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='\u0627\u0644\u062c\u0646\u062f\u0631', choices=[('F', '\u0623\u0646\u062b\u0649'), ('M', '\u0630\u0643\u0631')]),
        ),
        migrations.AlterField(
            model_name='registration',
            name='interview',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u062a\u0642\u0628\u0644 \u0628\u0639\u0645\u0644 \u0645\u0642\u0627\u0628\u0644\u0627\u062a \u0645\u0639\u0643 \u0642\u0628\u0644 \u0648 \u0628\u0639\u062f \u0627\u0644\u062d\u062f\u062b\u061f'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='job_title',
            field=models.CharField(max_length=100, null=True, verbose_name='\u0627\u0644\u0645\u0633\u0645\u0649 \u0627\u0644\u0648\u0638\u064a\u0641\u064a', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='meaning',
            field=models.TextField(null=True, verbose_name='\u0645\u0627 \u0627\u0644\u0630\u064a \u062a\u0639\u0646\u064a\u0647 \u0644\u0643 \u0639\u0628\u0627\u0631\u0629 \u0644\u0648 \u0623\u0646\u061f', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='mobile',
            field=models.CharField(max_length=20, null=True, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u062c\u0648\u0627\u0644', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='\u0627\u0633\u0645\u0643', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='past_experience',
            field=models.TextField(null=True, verbose_name='\u062a\u062d\u062f\u062b \u0639\u0646 \u062a\u062c\u0631\u0628\u062a\u0643 \u0627\u0644\u0633\u0627\u0628\u0642\u0629 \u0645\u0639 \u062a\u062f\u0643\u0633', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='referral',
            field=models.CharField(max_length=20, null=True, verbose_name='\u0643\u064a\u0641 \u0633\u0645\u0639\u062a \u0639\u0646 TEDxKSAUHS?', blank=True),
        ),
        migrations.AlterField(
            model_name='registration',
            name='take_pic',
            field=models.BooleanField(default=False, verbose_name='\u0647\u0644 \u062a\u0642\u0628\u0644 \u0628\u0627\u0644\u062a\u0635\u0648\u064a\u0631 \u0623\u062b\u0646\u0627\u0621 \u0627\u0644\u062d\u062f\u062b\u061f'),
        ),
        migrations.AlterField(
            model_name='registration',
            name='your_interest',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='\u0627\u064a \u0627\u0644\u0645\u062c\u0627\u0644\u0627\u062a \u0627\u0644\u062a\u0627\u0644\u064a\u0629 \u0623\u0642\u0631\u0628 \u0644\u0627\u0647\u062a\u0645\u0627\u0645\u0643\u061f', choices=[('A', '\u0627\u0644\u0641\u0646'), ('E', '\u0627\u0644\u062a\u0639\u0644\u064a\u0645'), ('H', '\u0627\u0644\u0635\u062d\u0629'), ('T', '\u0627\u0644\u062a\u0643\u0646\u0648\u0644\u0648\u062c\u064a\u0627'), ('S', '\u0627\u0644\u0631\u064a\u0627\u0636\u0629'), ('B', '\u0631\u064a\u0627\u062f\u0629 \u0627\u0644\u0623\u0639\u0645\u0627\u0644'), ('V', '\u0627\u0644\u062a\u0637\u0648\u0639'), ('M', '\u0627\u0644\u062a\u0633\u0648\u064a\u0642'), ('L', '\u0627\u0644\u0623\u062f\u0628')]),
        ),
        migrations.AlterField(
            model_name='registration',
            name='yourself',
            field=models.TextField(null=True, verbose_name='\u062a\u062d\u062f\u062b \u0639\u0646 \u0646\u0641\u0633\u0643', blank=True),
        ),
    ]
