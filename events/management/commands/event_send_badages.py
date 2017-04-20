import time

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import translation

from events.models import Event
from events import utils
from post_office import mail


class Command(BaseCommand):
    help = "Send badges emails."
    def add_arguments(self, parser):
        parser.add_argument('--event-code-name', dest='event_code_name',
                            type=str)
        parser.add_argument('--sleep-time', dest='sleep_time',
                default=None, type=int)

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        event = Event.objects.get(code_name=options['event_code_name'])
        event_users = User.objects.filter(session_registrations__session__event=event,
                                          session_registrations__is_deleted=False)\
                                  .distinct()
                                  #.exclude(session_registrations__badge_sent=False)\
        domain = Site.objects.get_current().domain
        my_registration_url = "https://{}{}".format(domain,
                                                    reverse('events:list_my_registration'))
        for user in event_users.iterator():
            if not utils.email_badge(user, event, my_registration_url):
                print "Erorr with {}'s email: {}".format(user.username, user.email)
                continue

            user.session_registrations.filter(is_deleted=False, session__event=event).update(badge_sent=True)

            self.stdout.write("Sent to {}!".format(user.email))

            if options['sleep_time']:
                time.sleep(options['sleep_time'])
