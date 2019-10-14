# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_add_2018_2019_year'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HPCPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('title', models.CharField(max_length=200, null=True, verbose_name='\u0627\u0644\u0644\u0642\u0628', blank=True)),
                ('photo', models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629', blank=True)),
                ('role', models.CharField(max_length=1, verbose_name='\u062f\u0648\u0631 \u0627\u0644\u0641\u0631\u062f \u0641\u064a \u0627\u0644\u0645\u0624\u062a\u0645\u0631', choices=[('L', '\u0642\u0627\u0626\u062f/\u0629'), ('S', '\u0645\u062a\u062d\u062f\u062b\u0640/\u0640\u0629'), ('W', '\u0641\u0627\u0626\u0632/\u0629')])),
            ],
            options={
                'verbose_name': '\u0641\u0631\u062f \u0645\u0646 \u0627\u0644\u0645\u0624\u062a\u0645\u0631',
                'verbose_name_plural': '\u0623\u0641\u0631\u0627\u062f \u0627\u0644\u0645\u0624\u062a\u0645\u0631 ',
            },
        ),
        migrations.CreateModel(
            name='HPCVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645')),
                ('version_number', models.CharField(max_length=100, null=True, verbose_name='\u0631\u0642\u0645 \u0627\u0644\u0646\u0633\u062e\u0629', blank=True)),
                ('logo', models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0634\u0639\u0627\u0631', blank=True)),
                ('vision', models.TextField(null=True, verbose_name='\u0627\u0644\u0631\u0624\u064a\u0629', blank=True)),
                ('mission', models.TextField(null=True, verbose_name='\u0627\u0644\u0647\u062f\u0641', blank=True)),
                ('other_comment', models.TextField(null=True, verbose_name='\u062a\u0639\u0644\u064a\u0642 \u0622\u062e\u0631', blank=True)),
                ('year', models.OneToOneField(verbose_name='\u0627\u0644\u0633\u0646\u0629 \u0627\u0644\u062f\u0631\u0627\u0633\u064a\u0629', to='core.StudentClubYear')),
            ],
            options={
                'verbose_name': '\u0646\u0633\u062e\u0629',
                'verbose_name_plural': '\u0646\u0633\u062e \u0627\u0644\u0645\u0624\u062a\u0645\u0631',
            },
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=300, verbose_name='\u0627\u0644\u0648\u0635\u0641')),
                ('number', models.IntegerField(verbose_name='\u0627\u0644\u0631\u0642\u0645')),
                ('icon', models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0623\u064a\u0642\u0648\u0646\u0629', blank=True)),
                ('hpc_version', models.ForeignKey(verbose_name='\u0627\u0644\u0646\u0633\u062e\u0629', to='hpc_temp.HPCVersion')),
            ],
            options={
                'verbose_name': '\u0625\u062d\u0635\u0627\u0626\u064a\u0629',
                'verbose_name_plural': '\u0625\u062d\u0635\u0627\u0626\u064a\u0627\u062a',
            },
        ),
        migrations.CreateModel(
            name='Winner',
            fields=[
                ('hpcperson_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='hpc_temp.HPCPerson')),
                ('section', models.CharField(max_length=1, verbose_name='\u0627\u0644\u0645\u0633\u0627\u0631', choices=[('O', '\u0627\u0644\u0639\u0631\u0648\u0636 \u0627\u0644\u0628\u062d\u062b\u064a\u0629'), ('P', '\u0627\u0644\u0645\u0644\u0635\u0642\u0627\u062a \u0627\u0644\u0628\u062d\u062b\u064a\u0629')])),
                ('rank', models.CharField(blank=True, max_length=1, null=True, verbose_name='\u0627\u0644\u0645\u0631\u062a\u0628\u0629', choices=[('1', '\u0627\u0644\u0645\u0631\u0643\u0632 \u0627\u0644\u0623\u0648\u0644'), ('2', '\u0627\u0644\u0645\u0631\u0643\u0632 \u0627\u0644\u062b\u0627\u0646\u064a'), ('3', '\u0627\u0644\u0645\u0631\u0643\u0632 \u0627\u0644\u062b\u0627\u0644\u062b')])),
            ],
            options={
                'verbose_name': '\u0641\u0627\u0626\u0632',
                'verbose_name_plural': '\u0627\u0644\u0641\u0627\u0626\u0632\u064a\u0646',
            },
            bases=('hpc_temp.hpcperson',),
        ),
        migrations.AddField(
            model_name='hpcperson',
            name='user',
            field=models.OneToOneField(null=True, blank=True, to=settings.AUTH_USER_MODEL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629'),
        ),
    ]
