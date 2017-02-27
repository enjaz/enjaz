# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_answer', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('right_answers', models.IntegerField(default=0)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('choices', models.ForeignKey(to='questions.Choice', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_type', models.CharField(default=b'S', max_length=1, verbose_name='\u0646\u0648\u0639 \u0627\u0644\u0633\u0624\u0627\u0644', choices=[(b'F', '\u0627\u0631\u0628\u0639 \u0635\u0648\u0631'), (b'Q', '\u0633\u0624\u0627\u0644'), (b'S', '\u0644\u0642\u0637\u0647')])),
                ('text', models.CharField(max_length=200)),
                ('booth', models.ForeignKey(to='questions.Booth', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionFigure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('figure', models.FileField(null=True, upload_to=b'questions/question_image', blank=True)),
                ('question', models.ForeignKey(to='questions.Question')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(to='questions.Question'),
        ),
    ]
