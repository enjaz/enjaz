# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0057_certificates'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='mandotary_survey',
            field=models.ForeignKey(related_name='mandotary_surveys', to='events.Survey', null=True),
        ),
        migrations.AddField(
            model_name='session',
            name='optional_survey',
            field=models.ForeignKey(related_name='optional_surveys', to='events.Survey', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='coauthor_certificate_template',
            field=models.ForeignKey(related_name='coauthor_events', verbose_name='\u0642\u0627\u0644\u0628 \u0634\u0647\u0627\u062f\u0629 \u0627\u0644\u0645\u0634\u0627\u0631\u0643\u0629 \u0641\u064a \u0627\u0644\u062a\u0623\u0644\u064a\u0641', blank=True, to='certificates.CertificateTemplate', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_certificate_template',
            field=models.ForeignKey(related_name='events', verbose_name='\u0642\u0627\u0644\u0628 \u0634\u0647\u0627\u062f\u0629 \u0627\u0644\u062d\u062f\u062b', blank=True, to='certificates.CertificateTemplate', null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='oral_certificate_template',
            field=models.ForeignKey(related_name='oral_events', verbose_name='\u0642\u0627\u0644\u0628 \u0634\u0647\u0627\u062f\u0629 \u0627\u0644\u062a\u0642\u062f\u064a\u0645 \u0627\u0644\u0634\u0641\u0647\u064a', blank=True, to='certificates.CertificateTemplate', null=True),
        ),
    ]
