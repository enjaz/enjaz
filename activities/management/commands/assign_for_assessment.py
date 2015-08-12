from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from activities.models import Activity
from core.models import StudentClubYear
from clubs.models import Club
from django.utils import timezone
from post_office import mail


class Command(BaseCommand):
    help = 'Assign activities that have been conducted to the appropriate assessor.'

    def handle(self, *args, **options):
        current_year = StudentClubYear.objects.get_current() 
        media_centers = Club.objects.filter(year=current_year, english_name__contains="Media Center", can_assess=True)
        presidencies = Club.objects.filter(year=current_year, english_name__contains="Presidency", can_assess=True)
        now = timezone.now()
        for activity in Activity.objects.current_year().approved().filter(assignee__isnull=True).exclude(episode__end_date__gt=now).exclude(assessment__assessor_club__in=presidencies).distinct():
            media_center = activity.get_media_assessor()
            presidency = activity.get_presidency_assessor()
            activity.assignee = presidency
            domain = Site.objects.get_current().domain
            email_context = {'activity': activity}
            if presidency.coordinator:
                full_url = "https://{}{}".format(domain,
                                                 reverse('activities:assess',
                                                         args=(activity.pk, 'p')))
                email_context['full_url'] = full_url
                email_context['assessor_club'] =  presidency
                mail.send([presidency.coordinator.email],
                           template="activity_done_to_assessor",
                           context=email_context)
            if media_center.coordinator:
                full_url = "https://{}{}".format(domain,
                                                 reverse('activities:assess',
                                                         args=(activity.pk, 'm')))
                email_context['full_url'] = full_url
                email_context['assessor_club'] =  media_center
                mail.send([media_center.coordinator.email],
                           template="activity_done_to_assessor",
                           context=email_context)            
            self.stdout.write(u'Assigned {0} to {1}. Emailing both {1} and {2}.'.format(activity.name, presidency, media_center))
            activity.save()
