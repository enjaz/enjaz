import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import translation

from certificates.models import Certificate, CertificateTemplate
from events.models import Event, Abstract
from post_office import mail


class Command(BaseCommand):
    help = "Send badges emails."
    def add_arguments(self, parser):
        parser.add_argument('--event-code-name', dest='event_code_name',
                            type=str)
        parser.add_argument('--oral-template-pk', dest='oral_template_pk',
                            type=int)
        parser.add_argument('--poster-template-pk', dest='poster_template_pk',
                            type=int)
        parser.add_argument('--send-emails', dest='send_emails',
                            action='store_true', default=False)

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        event = Event.objects.get(code_name=options['event_code_name'])
        from_email = event.get_notification_email()
        # Skip abstracts that already have certificates
        generated_pks = Certificate.objects.values_list('abstracts__pk', flat=True)
        abstracts = Abstract.objects.filter(event=event,
                                            user__isnull=False,
                                            did_presenter_attend=True,
                                            accepted_presentaion_preference__in=["O", "P"])\
                                    .exclude(pk__in=generated_pks)
        template = CertificateTemplate.objects.get(pk=options['certificate_template'])
        domain = Site.objects.get_current().domain
        url = "https://{}{}".format(domain,
                                    reverse('certificates:list_certificates_per_user'))
        for abstract in abstracts:
            template.generate_certificate(abstract.user, [abstract.user.get_en_full_name(), abstract.title])
            if options['send_emails']:
                contxt = {'title': abstract.title,
                          'user': abstract.user,
                          'event': event,
                          'url': url}
                mail.send(abstract.email, from_email,
                          template='event_abstract_certificate',
                          context=context)
