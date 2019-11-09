from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import translation

from events.models import Event, Abstract
from post_office import mail
from certificates.models import Certificate


class Command(BaseCommand):
    help = "Send badges emails."
    def add_arguments(self, parser):
        parser.add_argument('--event-code-name', dest='event_code_name',
                            type=str)
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
        domain = Site.objects.get_current().domain
        url = "https://{}{}".format(domain,
                                    reverse('certificates:list_certificates_per_user'))
        for abstract in abstracts:
            if abstract.accepted_presentaion_preference == 'O':
                template = abstract.event.oral_certificate_template
            elif abstract.accepted_presentaion_preference == 'P':
                template = abstract.event.poster_certificate_template

            template.generate_certificate(abstract.user, [abstract.presenting_author, abstract.title])
            if options['send_emails']:
                contxt = {'title': abstract.title,
                          'user': abstract.user,
                          'event': event,
                          'url': url}
                mail.send(abstract.email, from_email,
                          template='event_abstract_certificate',
                          context=context)
