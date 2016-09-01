# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bulb', '0015_initial_borrowing_balance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recruitment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prefers_coordination', models.BooleanField(default=False)),
                ('prefers_team_membership', models.BooleanField(default=False)),
                ('prefers_alone', models.BooleanField(default=False)),
                ('wants_book_contribution', models.BooleanField(default=False)),
                ('book_estimate', models.PositiveIntegerField(blank=True, null=True)),
                ('wants_book_exchange_organization', models.BooleanField(default=False)),
                ('reading_group_subjects', models.TextField(blank=True)),
                ('wants_reading_group_coordination', models.BooleanField(default=False)),
                ('wants_reading_group_organization', models.BooleanField(default=False)),
                ('debate_subjects', models.TextField(blank=True)),
                ('watns_debate_participation', models.BooleanField(default=False)),
                ('wants_debate_organization', models.BooleanField(default=False)),
                ('dewanya_subjects', models.TextField(blank=True)),
                ('dewanya_guests', models.TextField(blank=True)),
                ('wants_dewanya_organization', models.BooleanField(default=False)),
                ('wants_media_design', models.BooleanField(default=False)),
                ('example_design', models.FileField(upload_to=b'bulb_design_examples', blank=True)),
                ('wants_media_video', models.BooleanField(default=False)),
                ('wants_media_photography', models.BooleanField(default=False)),
                ('interests', models.TextField(blank=True)),
                ('goals', models.TextField(blank=True)),
                ('activities', models.TextField(blank=True)),
                ('twitter', models.CharField(max_length=200, blank=True)),
                ('goodreads', models.URLField(blank=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('user', models.ForeignKey(related_name='bulb_recruitment', verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
