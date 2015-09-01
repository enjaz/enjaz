import datetime
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from activities.models import Activity
from django.utils import timezone
from post_office import mail


class Command(BaseCommand):
    help = 'Assign activities that have been conducted to the appropriate assessor.'

    def handle(self, *args, **options):
        domain = Site.objects.get_current().domain
        end_date_target = timezone.now().date()
        end_time_since = (timezone.now() - datetime.timedelta(minutes=10)).time()
        end_time_until = timezone.now().time()
        for activity in Activity.objects.current_year().approved().filter(episode__end_date=end_date_target)\
                                                                  .filter(episode__end_time__gt=end_time_since,
                                                                          episode__end_time__lte=end_time_until)\
                                                                  .filter(episode__followupreport__isnull=True).distinct():
            email_context = {'activity': activity}
            if activity.primary_club.media_representatives.exists():
                to = [user.email for user in activity.primary_club.media_representatives.all()]
            elif activity.primary_club.coordinator:
                to = [activity.primary_club.coordinator.email]
            else:
                continue

            # Allow for the possibility of multiple episodes ending on
            # the same day.
            full_urls = ""

            for episode in targeted_episodes:
                full_url = "https://{}{}".format(domain,
                                                 reverse('media:submit_report',
                                                         args=(episode.pk,)))
                full_urls += full_url + "\n"

            email_context['full_urls'] = full_urls
            mail.send(to,
                      template="episode_done_to_media_representative",
                      context=email_context)
            self.stdout.write(u"Activity {} is done.  Emailing {}.".format(activity.name, ", ".join(to)))
