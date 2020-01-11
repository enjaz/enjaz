# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContestAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0646\u0635 \u0627\u0644\u062c\u0648\u0627\u0628')),
                ('is_correct', models.BooleanField(default=False, verbose_name='\u0647\u0644 \u0627\u0644\u062c\u0648\u0627\u0628 \u0635\u062d\u064a\u062d\u061f')),
            ],
            options={
                'verbose_name': '\u062c\u0648\u0627\u0628',
                'verbose_name_plural': '\u0623\u062c\u0648\u0628\u0629',
            },
        ),
        migrations.CreateModel(
            name='ContestQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(verbose_name='\u0646\u0635 \u0627\u0644\u0633\u0624\u0627\u0644')),
                ('category', models.CharField(max_length=100, verbose_name='\u0646\u0635 \u0627\u0644\u0633\u0624\u0627\u0644')),
                ('olympiad_version', models.CharField(max_length=100, null=True, verbose_name='\u0646\u0633\u062e\u0629 \u0627\u0644\u0623\u0648\u0644\u0645\u0628\u064a\u0627\u062f')),
            ],
            options={
                'verbose_name': '\u0633\u0624\u0627\u0644',
                'verbose_name_plural': '\u0623\u0633\u0626\u0644\u0629',
            },
        ),
        migrations.CreateModel(
            name='Inventor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ar_name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u062b\u0644\u0627\u062b\u064a \u0628\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0639\u0631\u0628\u064a\u0629')),
                ('en_name', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0627\u0633\u0645 \u0627\u0644\u062b\u0644\u0627\u062b\u064a \u0628\u0627\u0644\u0644\u063a\u0629 \u0627\u0644\u0625\u0646\u062c\u0644\u064a\u0632\u064a\u0629')),
                ('job', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0648\u0638\u064a\u0641\u0629')),
                ('workplace', models.CharField(max_length=200, verbose_name='\u062c\u0647\u0629 \u0627\u0644\u0639\u0645\u0644/\u0627\u0644\u062f\u0631\u0627\u0633\u0629')),
                ('invention_name', models.CharField(max_length=600, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u0627\u062e\u062a\u0631\u0627\u0639')),
                ('inv_category', multiselectfield.db.fields.MultiSelectField(max_length=91, verbose_name='\u0627\u0644\u062a\u0635\u0646\u064a\u0641 (\u064a\u0645\u0643\u0646 \u0627\u062e\u062a\u064a\u0627\u0631 \u0623\u0643\u062b\u0631 \u0645\u0646 \u062a\u0635\u0646\u064a\u0641)', choices=[('anm', '\u0639\u0644\u0648\u0645 \u0627\u0644\u062d\u064a\u0648\u0627\u0646'), ('bhv', '\u0627\u0644\u0639\u0644\u0648\u0645 \u0627\u0644\u0627\u062c\u062a\u0645\u0627\u0639\u064a\u0629 \u0648\u0627\u0644\u0633\u0644\u0648\u0643\u064a\u0629'), ('bch', '\u0627\u0644\u0643\u064a\u0645\u064a\u0627\u0621 \u0627\u0644\u062d\u064a\u0648\u064a\u0629'), ('bmd', '\u0627\u0644\u0639\u0644\u0648\u0645 \u0627\u0644\u0637\u0628\u064a\u0629 \u0627\u0644\u062d\u064a\u0648\u064a\u0629 \u0648\u0627\u0644\u0635\u062d\u064a\u0629'), ('mde', '\u0627\u0644\u0647\u0646\u062f\u0633\u0629 \u0627\u0644\u0637\u0628\u064a\u0629 \u0627\u0644\u062d\u064a\u0648\u064a\u0629'), ('cbi', '\u0627\u0644\u0623\u062d\u064a\u0627\u0621 \u0627\u0644\u062e\u0644\u0648\u064a\u0629 \u0648\u0627\u0644\u062c\u0632\u064a\u0626\u064a\u0629'), ('chm', '\u0627\u0644\u0643\u064a\u0645\u064a\u0627\u0621'), ('bit', '\u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a\u064a\u0629 \u0627\u0644\u062d\u064a\u0648\u064a\u0629'), ('eco', '\u0639\u0644\u0648\u0645 \u0627\u0644\u0623\u0631\u0636 \u0648\u0627\u0644\u0628\u064a\u0626\u0629'), ('emb', '\u0627\u0644\u0623\u0646\u0638\u0645\u0629 \u0627\u0644\u0645\u062f\u0645\u062c\u0629'), ('che', '\u0627\u0644\u0637\u0627\u0642\u0629 \u0627\u0644\u0643\u064a\u0645\u064a\u0627\u0626\u064a\u0629'), ('phe', '\u0627\u0644\u0637\u0627\u0642\u0629 \u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0626\u064a\u0629'), ('mch', '\u0627\u0644\u0647\u0646\u062f\u0633\u0629 \u0627\u0644\u0645\u064a\u0643\u0627\u0646\u064a\u0643\u064a\u0629'), ('ene', '\u0627\u0644\u0647\u0646\u062f\u0633\u0629 \u0627\u0644\u0628\u064a\u0626\u064a\u0629'), ('smt', '\u0639\u0644\u0645 \u0627\u0644\u0645\u0648\u0627\u062f'), ('mat', '\u0627\u0644\u0631\u064a\u0627\u0636\u064a\u0627\u062a'), ('mbi', '\u0627\u0644\u0623\u062d\u064a\u0627\u0621 \u0627\u0644\u062f\u0642\u064a\u0642\u0629'), ('ast', '\u0627\u0644\u0641\u064a\u0632\u064a\u0627\u0621 \u0648\u0627\u0644\u0641\u0644\u0643'), ('bot', '\u0639\u0644\u0648\u0645 \u0627\u0644\u0646\u0628\u0627\u062a'), ('rai', '\u0627\u0644\u0631\u0628\u0648\u062a\u0627\u062a \u0648\u0627\u0644\u0630\u0643\u0627\u0621 \u0627\u0644\u0627\u0635\u0637\u0646\u0627\u0639\u064a'), ('prg', '\u0627\u0644\u0623\u0646\u0638\u0645\u0629 \u0627\u0644\u0628\u0631\u0645\u062c\u064a\u0629 \u0648\u0627\u0644\u0628\u0631\u0645\u062c\u0629'), ('mob', '\u0627\u0644\u0639\u0644\u0648\u0645 \u0627\u0644\u0637\u0628\u064a\u0629 \u0627\u0644\u0627\u0646\u062a\u0642\u0627\u0644\u064a\u0629'), ('oth', '\u062a\u0635\u0646\u064a\u0641 \u0622\u062e\u0631')])),
                ('other_category', models.CharField(max_length=600, null=True, verbose_name="\u0625\u0630\u0627 \u0627\u062e\u062a\u0631\u062a '\u062a\u0635\u0646\u064a\u0641 \u0622\u062e\u0631'\u060c \u0627\u0630\u0643\u0631\u0647 \u0647\u0646\u0627 ", blank=True)),
                ('summary', models.TextField(verbose_name='\u0645\u0644\u062e\u0635 \u0627\u0644\u0627\u062e\u062a\u0631\u0627\u0639')),
                ('is_prototype', models.BooleanField(verbose_name='\u0647\u0644 \u064a\u0648\u062c\u062f \u0644\u062f\u064a\u0643 \u0646\u0645\u0648\u0630\u062c \u0623\u0648\u0644\u064a\u061f')),
                ('prototype_file', models.FileField(upload_to=b'', null=True, verbose_name='\u0627\u0644\u0631\u062c\u0627\u0621 \u0625\u0631\u0641\u0627\u0642 \u0627\u0644\u0646\u0645\u0648\u0630\u062c \u0627\u0644\u0623\u0648\u0644\u064a \u0643\u0645\u0644\u0641 PDF \u0625\u0646 \u0648\u062c\u062f', blank=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0633\u062c\u064a\u0644')),
            ],
            options={
                'verbose_name': '\u0645\u062e\u062a\u0631\u0639',
                'verbose_name_plural': '\u0645\u062e\u062a\u0631\u0639\u064a\u0646',
            },
        ),
        migrations.AddField(
            model_name='contestanswer',
            name='question',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0633\u0624\u0627\u0644', to='science_olympiad.ContestQuestion'),
        ),
    ]
