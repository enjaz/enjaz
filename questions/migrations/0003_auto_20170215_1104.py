# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0002_auto_20170214_0552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('right_answers', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(to='questions.Answer', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='userresponse',
            name='user',
        ),
        migrations.RemoveField(
            model_name='questionfigure',
            name='upload',
        ),
        migrations.DeleteModel(
            name='UserResponse',
        ),
    ]
