# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_add_2nd_hpc'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractFigure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('figure', models.FileField(upload_to=b'hpc/figures/', verbose_name='Attach the figure')),
            ],
        ),
        migrations.RemoveField(
            model_name='abstract',
            name='attachment',
        ),
        migrations.AddField(
            model_name='abstract',
            name='conclusion',
            field=models.TextField(default=b'', verbose_name='Conclusion'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='discussion',
            field=models.TextField(default=b'', verbose_name='Discussion'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='introduction',
            field=models.TextField(default=b'', verbose_name='Introduction'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='methodology',
            field=models.TextField(default=b'', verbose_name='Methodology'),
        ),
        migrations.AddField(
            model_name='abstract',
            name='results',
            field=models.TextField(default=b'', verbose_name='Results'),
        ),
        migrations.AddField(
            model_name='abstractfigure',
            name='abstract',
            field=models.ForeignKey(related_name='figures', to='events.Abstract'),
        ),
    ]
