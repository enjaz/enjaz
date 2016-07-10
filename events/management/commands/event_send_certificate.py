import json
import urllib2
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.utils import translation

from events.models import Event, Registration
from post_office import mail

class Command(BaseCommand):
    help = "Send certificate emails."
    def add_arguments(self, parser):
        parser.add_argument('--event-pk', dest='event_pk',
                            default=None, type=int)
        parser.add_argument('--sleep-time', dest='sleep_time',
                            default=None, type=int)

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        event = Event.objects.get(pk=options['event_pk'])
        users = {}

        # Get programs
        for session in event.session_set.filter(vma_id__isnull=False):
            if session.vma_time_code:
                list_url = "http://www.medicalacademy.org/portal/list/attends/workshop/get/data?workshop_id="
            else:
                list_url = "http://www.medicalacademy.org/portal/list/attends/event/get/data?event_id="
            self.stdout.write(u"Getting {}...".format(session))
            url = list_url + str(session.vma_id)
            data = urllib2.urlopen(url)
            users[session.pk] = json.load(data)
            count = len(users[session.pk])
            self.stdout.write("We got {}.".format(count))

        for registration in Registration.objects.filter(moved_sessions__event=event,
                                                        is_deleted=False,
                                                        certificate_sent=False).distinct():
            user_certificates = {}
            for session in registration.moved_sessions.filter(vma_id__isnull=False):
                for user in users[session.pk]:
                    if user['email'].lower() == registration.get_email().lower():
                        filename = event.name + '-' + str(session.vma_id) + '.pdf'
                        certificate = urllib2.urlopen(user['certificate']).read()
                        attachment = ContentFile(certificate)
                        user_certificates[filename] = attachment
                        self.stdout.write("Found a certificate for {}!".format(user['email']))
                        break

            if not user_certificates:
                continue

            email_context = {'registration': registration,
                             'event': event}
            try:
                mail.send([registration.get_email()],
                          template="event_certificate",
                          context=email_context,
                          attachments=user_certificates)
            except ValidationError:
                print "Erorr with", user['email']

            registration.certificate_sent = True
            registration.save()

            self.stdout.write("Sent to {}!".format(registration.get_email()))
            if options['sleep_time']:
                time.sleep(options['sleep_time'])
