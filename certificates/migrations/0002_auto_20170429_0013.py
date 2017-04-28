# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TextPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('y_position', models.PositiveIntegerField(verbose_name='\u0627\u0644\u0645\u0648\u0636\u0639 \u0639\u0644\u0649 \u0627\u0644\u0645\u062d\u0648\u0631 \u0627\u0644\u0633\u064a\u0646\u064a')),
                ('x_position', models.PositiveIntegerField(verbose_name='\u0627\u0644\u0645\u0648\u0636\u0639 \u0639\u0644\u0649 \u0627\u0644\u0645\u062d\u0648\u0631 \u0627\u0644\u0635\u0627\u062f\u064a')),
                ('size', models.PositiveIntegerField(default=34, verbose_name='\u062d\u062c\u0645 \u0627\u0644\u062e\u0637')),
                ('color', models.CharField(default=b'000000', max_length=10, verbose_name='\u0644\u0648\u0646 \u0627\u0644\u062e\u0637')),
            ],
        ),
        migrations.RemoveField(
            model_name='certificate',
            name='email',
        ),
        migrations.RemoveField(
            model_name='certificatetemplate',
            name='color',
        ),
        migrations.RemoveField(
            model_name='certificatetemplate',
            name='font_size',
        ),
        migrations.RemoveField(
            model_name='certificatetemplate',
            name='x_position',
        ),
        migrations.RemoveField(
            model_name='certificatetemplate',
            name='y_position',
        ),
        migrations.AlterField(
            model_name='certificate',
            name='certificate_template',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0642\u0627\u0644\u0628', to='certificates.CertificateTemplate'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='image',
            field=models.ImageField(upload_to=b'', verbose_name='\u0627\u0644\u0635\u0648\u0631\u0629'),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='user',
            field=models.ForeignKey(verbose_name='\u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0640/\u0640\u0629', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='textposition',
            name='certificate_template',
            field=models.ForeignKey(related_name='text_positions', verbose_name='\u0627\u0644\u0642\u0627\u0644\u0628', to='certificates.CertificateTemplate'),
        ),
    ]
