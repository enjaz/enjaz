from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.utils import translation, timezone
from django.contrib.auth.models import User

from post_office import mail

class Command(BaseCommand):
    help = "Send reminding emails."

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        tomorrow_date = timezone.now().date() + timezone.timedelta(days=1)

        for user in User.objects.filter(session_registrations__session__date=tomorrow_date).distinct():
            tomorrow_registrations = user.session_registrations.filter(session__date=tomorrow_date)
            event = tomorrow_registrations.first().session.event
            print event
            
            try:
                first_name = user.common_profile.ar_first_name
            except ObjectDoesNotExist:
                first_name = user.username

            email_context = {'first_name': first_name,
                             'event': event,
                             'tomorrow_date': tomorrow_date,
                             'tomorrow_registrations':
                             tomorrow_registrations}
            mail.send([user.email],
                       template="event_session_reminder",
                       context=email_context)
