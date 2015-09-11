import datetime
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from activities.models import Activity
from clubs.models import Club
from django.utils import timezone
from post_office import mail


class Command(BaseCommand):
    help = 'Run every ten minutes to send the presidency assessment notifications.'

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        end_date_target = timezone.now().date()
        end_time_since = (timezone.now() - datetime.timedelta(minutes=10)).time()
        end_time_until = timezone.now().time()
        for activity in Activity.objects.current_year().approved().done().filter(episode__end_date=end_date_target)\
                                                                         .exclude(assessment__criterionvalue__criterion__category='P'):
            # If the activity didn't end within the past ten minutes,
            # skip, because another proccess would have sent a
            # notification about it.
            if not activity.episode_set.filter(episode__end_date=end_date_target,
                                               episode__end_time__gt=end_time_since,
                                               episode__end_time__lte=end_time_until).exists():
                continue
            email_context = {'activity': activity}
            assessor_club = Club.objects.club_assessing_parents(activity.primary_club).first()
            if assessor_club.coordinator:
                full_url = "https://{}{}".format(domain,
                                                 reverse('activities:assess',
                                                         args=(activity.pk, 'p')))
                email_context['full_url'] = full_url
                email_context['assessor_club'] =  assessor_club
                email_context['assessor'] = assessor_club.coordinator
                mail.send([assessor_club.coordinator.email],
                           template="activity_done_to_assessor",
                           context=email_context)
            self.stdout.write(u'Assigned {0} to {1}. Emailing {1}.'.format(activity.name, assessor_club))
