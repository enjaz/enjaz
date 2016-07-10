import json
import urllib2
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import translation

from events.models import Event, Registration
from post_office import mail

class Command(BaseCommand):
    help = "Send confirmation emails."

    def add_arguments(self, parser):
        parser.add_argument('--event-pk', dest='event_pk',
                            default=None, type=int)
        parser.add_argument('--sleep-time', dest='sleep_time',
                            default=None, type=int)
        parser.add_argument('--workshop-event-pk', dest='workshop_event_pk',
                            default=None, type=int)

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        users = {}
        event = Event.objects.get(pk=options['event_pk'])
        list_url = "http://medicalacademy.org/portal/list/registration/get/data?event_id="
        for session in event.session_set.filter(vma_id__isnull=False):
            self.stdout.write(u"Getting {}...".format(session))
            url = list_url + str(session.vma_id)
            data = urllib2.urlopen(url)
            users[session.vma_id] = json.load(data)
            count = len(users[session.vma_id])
            self.stdout.write(u"We got {}.".format(count))

        for registration in Registration.objects.filter(first_priority_sessions__event=event,
                                                        is_deleted=False,
                                                        reminder_sent=False,
                                                        moved_sessions__isnull=False).distinct():
            enjaz_sessions = registration.first_priority_sessions.all() | \
                             registration.second_priority_sessions.all()
            if not enjaz_sessions.exists():
                continue
            session_count = registration.moved_sessions.count()
            programs = []
            workshops = []
            others = []
            for session in registration.moved_sessions.all():
                if session.vma_time_code:
                    workshop_event_pk = options['workshop_event_pk']
                    for user in users[workshop_event_pk]:
                        if user['email'].lower() == registration.get_email().lower():
                            self.stdout.write("Workshop: Found {}!".format(user['email']))                    
                            workshops.append((session, user['confirmation_link']))
                            break
                elif session.vma_id:
                    for user in users[session.vma_id]:
                        if user['email'].lower() == registration.get_email().lower():
                            self.stdout.write("Program: Found {}!".format(user['email']))
                            programs.append((session, user['confirmation_link']))
                            break
                else:
                    others.append(session)

            email_context = {'registration': registration,
                             'session_count': session_count,
                             'event': event,
                             'programs': programs,
                             'workshops': workshops,
                             'others': others}

            mail.send([registration.get_email()],
                       template="event_registration_reminder",
                       context=email_context)
            registration.reminder_sent = True
            registration.save()

            self.stdout.write("Sent to {}!".format(registration.get_email()))
            if options['sleep_time']:
                time.sleep(options['sleep_time'])
