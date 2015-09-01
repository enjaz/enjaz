import datetime
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from activities.models import Activity
from django.utils import timezone
from post_office import mail
from media.utils import get_club_media_center


class Command(BaseCommand):
    help = 'Assign activities that have been conducted to the appropriate assessor.'

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        end_date_target = timezone.now().date() - datetime.timedelta(5)
        for activity in Activity.objects.current_year().approved().done().filter(episode__end_date=end_date_target)\
                                                                         .exclude(assessment__criterionvalue__criterion__category='M')\
                                                                         .exclude(primary_club__media_assessor__isnull=True):
            email_context = {'activity': activity}
            if activity.primary_club.media_assessor:
                full_url = "https://{}{}".format(domain,
                                                 reverse('activities:assess',
                                                         args=(activity.pk, 'm')))
                email_context['full_url'] = full_url
                email_context['assessor_club'] =  get_club_media_center(activity.primary_club)
                email_context['assessor'] = activity.primary_club.media_assessor
                mail.send([activity.primary_club.media_assessor.email],
                           template="activity_done_to_assessor",
                           context=email_context)
            self.stdout.write(u'Assigned {0} to {1}. Emailing {1}.'.format(activity.name, presidency))
