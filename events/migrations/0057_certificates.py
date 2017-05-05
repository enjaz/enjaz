# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0002_add_fonts'),
        ('events', '0056_survery'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionregistration',
            name='certificate_sent',
        ),
        migrations.AddField(
            model_name='event',
            name='coauthor_certificate_template',
            field=models.ForeignKey(related_name='coauthor_events', verbose_name='\u0642\u0627\u0644\u0628 \u0634\u0647\u0627\u062f\u0629 \u0627\u0644\u0645\u0644\u0635\u0642 \u0627\u0644\u0628\u062d\u062b', blank=True, to='certificates.CertificateTemplate', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='event_certificate_template',
            field=models.ForeignKey(related_name='events', verbose_name='\u0642\u0627\u0644\u0628 \u0634\u0647\u0627\u062f\u0629 \u0627\u0644\u0645\u0644\u0635\u0642 \u0627\u0644\u0628\u062d\u062b', blank=True, to='certificates.CertificateTemplate', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='oral_certificate_template',
            field=models.ForeignKey(related_name='oral_events', verbose_name='\u0642\u0627\u0644\u0628 \u0634\u0647\u0627\u062f\u0629 \u0627\u0644\u0645\u0644\u0635\u0642 \u0627\u0644\u0628\u062d\u062b', blank=True, to='certificates.CertificateTemplate', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='poster_certificate_template',
            field=models.ForeignKey(related_name='poster_events', verbose_name='\u0642\u0627\u0644\u0628 \u0634\u0647\u0627\u062f\u0629 \u0627\u0644\u0645\u0644\u0635\u0642 \u0627\u0644\u0628\u062d\u062b', blank=True, to='certificates.CertificateTemplate', null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='certificate_template',
            field=models.ForeignKey(verbose_name='\u0642\u0627\u0644\u0628 \u0634\u0647\u0627\u062f\u0629 \u0627\u0644\u062c\u0644\u0633\u0629', blank=True, to='certificates.CertificateTemplate', null=True),
        ),
        migrations.AlterField(
            model_name='abstract',
            name='accepted_presentaion_preference',
            field=models.CharField(blank=True, max_length=1, verbose_name=b'Accepted presentation preference', choices=[(b'O', b'Oral'), (b'P', b'Poster')]),
        ),
    ]
