from django.core.management.base import BaseCommand
from activities.models import Activity
from core.models import StudentClubYear
from clubs.models import Club
from django.utils import timezone


class Command(BaseCommand):
    help = 'Assign activities that have been conducted to the appropriate assessor.'

    def handle(self, *args, **options):
        current_year = StudentClubYear.objects.get_current() 
        presidencies = Club.objects.filter(year=current_year, english_name__contains="Presidency", can_assess=True)
        media_centers = Club.objects.filter(year=current_year, english_name__contains="Media Center", can_assess=True)
        now = timezone.now()
        for activity in Activity.objects.current_year().approved().filter(assignee__isnull=True).exclude(episode__end_date__gt=now).exclude(assessment__assessor_club__in=media_centers).distinct():
            if activity.primary_club.city == 'R' and activity.primary_club.gender:
                media_center = media_centers.get(city='R', gender=activity.primary_club.gender)
            elif activity.primary_club.city == 'R' and not activity.primary_club.gender:  # Presidency activities
                media_center = media_centers.get(city='R', gender='M')
            else:
                media_center = media_centers.get(city=activity.primary_club.city)
            self.stdout.write(u'Assigned {} to {}'.format(activity.name, media_center))
            activity.assignee = media_center
            activity.save()
        for activity in Activity.objects.current_year().approved().filter(assignee__isnull=True).exclude(episode__end_date__gt=now).exclude(assessment__assessor_club__in=presidencies).distinct():
            if activity.primary_club.city == 'R' and activity.primary_club.gender:
                presidency = presidencies.get(city='R', gender=activity.primary_club.gender)
            elif activity.primary_club.city == 'R' and not activity.primary_club.gender:  # Presidency activities
                presidency = presidencies.get(city='R', gender='M')
            else:
                presidency = presidencies.get(city=activity.primary_club.city)
            self.stdout.write(u'Assigned {} to {}'.format(activity.name, presidency))
            activity.assignee = presidency
            activity.save()

            
            
