# -*- coding: utf-8  -*-
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
import accounts.utils


class Command(BaseCommand):
    help = "Send certificate emails."
    def add_arguments(self, parser):
        parser.add_argument('--event-code-name', dest='event_code_name',
                            type=str)
        parser.add_argument('--sleep-time', dest='sleep_time',
                default=None, type=int)

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        event = Event.objects.get(code_name=options['event_code_name'])
        event_users = (User.objects.filter(certificate__sessions__event=event) | \
                       User.objects.filter(certificate__abstracts__event=event)).distinct()
        count = 1
        self.stdout.write("We got {} users to handle!".format(event_users.count()))
        domain = Site.objects.get_current().domain
        url = "https://{}{}".format(domain,
                                    reverse('certificates:list_certificates_per_user'))
        for user in event_users.iterator():
            email_context = {'user': user,
                             'url': url,
                             'event': event}
            notification_email = event.get_notification_email()
            cc = accounts.utils.get_user_cc(user)
            mail.send([user.email],
                      u"بوابة إنجاز <{}>".format(notification_email),
                      cc=cc,
                      template="event_certificates",
                      context=email_context)

            self.stdout.write("{:06d}: Sent to {}!".format(count, user.email))
            count +=1
            if options['sleep_time']:
                time.sleep(options['sleep_time'])
