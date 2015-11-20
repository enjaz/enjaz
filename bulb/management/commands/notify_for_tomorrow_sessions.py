import datetime
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from bulb.models import Session
from django.utils import timezone
from post_office import mail
from bulb import utils


class Command(BaseCommand):
    help = "Notify users on session occurring tomorrow."

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        date = timezone.now().date() + datetime.timedelta(1)
        for session in Session.objects.filter(date=date, is_deleted=False):
            full_url = "https://{}{}#session-{}".format(domain,
                                                        reverse('bulb:show_group', args=(session.group.pk,)),
                                                        session.pk)
            email_context = {'session': session, 'full_url': full_url}
            for membership in session.group.membership_set.filter(is_active=True):
                email_context['member'] = membership.user
                mail.send([membership.user.email],
                           template="reading_group_session_reminder",
                           context=email_context)
                self.stdout.write(u'Emailed {} on {}.'.format(membership.user.username,
                                                                     session.title))

            # Also, send it to the Bulb coordinator.
            bulb_coordinator = utils.get_bulb_club_for_user(session.group.coordinator).coordinator
            mail.send([bulb_coordinator.email],
                       template="reading_group_session_reminder",
                       context=email_context)
