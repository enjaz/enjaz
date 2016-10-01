# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0005_update_student_report'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name': '\u062e\u0628\u0631', 'verbose_name_plural': '\u0627\u0644\u0623\u062e\u0628\u0627\u0631', 'permissions': (('view_story', 'Can view all available stories.'), ('edit_story', 'Can edit any available story.'), ('review_story', 'Can review any available story.'), ('assign_review_story', 'Can assign members to review stories.'))},
        ),
        migrations.AlterModelOptions(
            name='storyreview',
            options={'verbose_name': '\u0645\u0631\u0627\u062c\u0639\u0629 \u062e\u0628\u0631', 'verbose_name_plural': '\u0645\u0631\u0627\u062c\u0639\u0627\u062a \u0627\u0644\u0623\u062e\u0628\u0627\u0631'},
        ),
        migrations.AlterModelOptions(
            name='storytask',
            options={'verbose_name': '\u0645\u0647\u0645\u0629 \u062e\u0628\u0631', 'verbose_name_plural': '\u0645\u0647\u0645\u0627\u062a \u0627\u0644\u0623\u062e\u0628\u0627\u0631'},
        ),
        migrations.AlterField(
            model_name='story',
            name='date_submitted',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0631\u0641\u0639 \u0627\u0644\u062e\u0628\u0631'),
        ),
        migrations.AlterField(
            model_name='storyreview',
            name='story',
            field=models.OneToOneField(verbose_name='\u0627\u0644\u062e\u0628\u0631', to='media.Story'),
        ),
    ]
