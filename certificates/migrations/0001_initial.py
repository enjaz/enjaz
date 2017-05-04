# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0041_add_jeddah_criteria'),
        ('clubs', '0052_presidencies_can_assess'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'', verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629')),
                ('verification_code', models.CharField(max_length=6, verbose_name='\u0631\u0645\u0632 \u0627\u0644\u062a\u062d\u0642\u0642')),
                ('description', models.CharField(default=b'', max_length=200, verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0634\u0647\u0627\u062f\u0629', blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
            ],
        ),
        migrations.CreateModel(
            name='CertificateRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0634\u0647\u0627\u062f\u0629')),
                ('text', models.TextField(verbose_name='\u0627\u0644\u0635\u064a\u0627\u063a\u0629')),
                ('user_list', models.FileField(upload_to=b'certificate_lists', verbose_name='\u0642\u0627\u0626\u0645\u0629 \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u064a\u0646 \u0648\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0627\u062a', blank=True)),
                ('is_approved', models.NullBooleanField(default=None)),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('episode', models.ForeignKey(blank=True, to='activities.Episode', null=True)),
                ('submitter', models.ForeignKey(related_name='certificate_submissions', to=settings.AUTH_USER_MODEL)),
                ('submitter_club', models.ForeignKey(blank=True, to='clubs.Club', null=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0648\u0646 \u0648\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0627\u062a', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CertificateTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200, verbose_name='\u0648\u0635\u0641 \u0627\u0644\u0634\u0647\u0627\u062f\u0629')),
                ('image', models.ImageField(upload_to=b'certificate_templates', verbose_name='\u0635\u0648\u0631\u0629 \u0627\u0644\u0642\u0627\u0644\u0628')),
                ('image_format', models.CharField(default=b'PNG', max_length=10, verbose_name='\u0646\u0633\u0642 \u0627\u0644\u0635\u0648\u0631\u0629', choices=[(b'PNG', b'PNG'), (b'GIF', b'GIF'), (b'JPG', b'JPG')])),
                ('submission_date', models.DateTimeField(auto_now_add=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u0625\u0631\u0633\u0627\u0644')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='\u062a\u0627\u0631\u064a\u062e \u0627\u0644\u062a\u0639\u062f\u064a\u0644')),
                ('certificate_request', models.OneToOneField(null=True, blank=True, to='certificates.CertificateRequest')),
            ],
        ),
        migrations.CreateModel(
            name='CertificateText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200, verbose_name='\u0627\u0644\u0646\u0635')),
                ('certificate', models.ForeignKey(related_name='texts', verbose_name='\u0627\u0644\u0634\u0647\u0627\u062f\u0629', to='certificates.Certificate')),
            ],
        ),
        migrations.CreateModel(
            name='FontFamily',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='\u0627\u0633\u0645 \u0627\u0644\u062e\u0637')),
            ],
        ),
        migrations.CreateModel(
            name='TextPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('y_position', models.PositiveIntegerField(verbose_name='\u0627\u0644\u0645\u0648\u0636\u0639 \u0639\u0644\u0649 \u0627\u0644\u0645\u062d\u0648\u0631 \u0627\u0644\u0633\u064a\u0646\u064a')),
                ('x_center', models.BooleanField(default=False, verbose_name='\u0627\u0646\u062a\u0635\u0627\u0641 \u0633\u064a\u0646\u064a')),
                ('x_position', models.PositiveIntegerField(verbose_name='\u0627\u0644\u0645\u0648\u0636\u0639 \u0639\u0644\u0649 \u0627\u0644\u0645\u062d\u0648\u0631 \u0627\u0644\u0635\u0627\u062f\u064a')),
                ('y_center', models.BooleanField(default=False, verbose_name='\u0627\u0646\u062a\u0635\u0627\u0641 \u0635\u0627\u062f\u064a')),
                ('size', models.PositiveIntegerField(default=34, verbose_name='\u062d\u062c\u0645 \u0627\u0644\u062e\u0637')),
                ('color', models.CharField(default=b'000000', max_length=10, verbose_name='\u0644\u0648\u0646 \u0627\u0644\u062e\u0637')),
                ('certificate_template', models.ForeignKey(related_name='text_positions', verbose_name='\u0627\u0644\u0642\u0627\u0644\u0628', to='certificates.CertificateTemplate')),
                ('font_family', models.ForeignKey(verbose_name='\u0627\u0644\u062e\u0637\u0651', to='certificates.FontFamily', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='certificate',
            name='certificate_template',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0642\u0627\u0644\u0628', blank=True, to='certificates.CertificateTemplate', null=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='certificate',
            name='user',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', to=settings.AUTH_USER_MODEL),
        ),
    ]
