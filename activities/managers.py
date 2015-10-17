from django.db import models
from django.db.models.aggregates import Count
from django.utils import timezone

from clubs.utils import is_coordinator_of_any_club, is_deputy_of_any_club, get_user_clubs, \
    get_user_coordination_and_deputyships
from accounts.utils import get_user_city, get_user_gender
from clubs.models import Club


class ActivityQuerySet(models.QuerySet):
    """
    Custom manager for Activity model with custom querysets
    for approved, pending, and rejected activities.
    """
    def approved(self):
        """
        Return a queryset of approved activities.
        """
        # An approved activity is one which:
        # (1) has a number of reviews equal to the number of its reviewer parents
        # (2) has all of its reviews approved

        # The following is dirty way of dealing with query sets, but this is the only way given the deep complexity
        # of this query

        # WARNING: lengthy run-time; not lazy

        return self.filter(is_deleted=False).filter(is_approved=True)

    def rejected(self):
        """
        Return a queryset of rejected activities.
        """
        return self.filter(is_deleted=False).filter(is_approved=False)

    def pending(self):
        """
        Return a queryset of pending activities.
        """
        # pending activities that are not deleted.

        return self.filter(is_deleted=False).filter(is_approved=None)

    def undeleted(self):
        return self.filter(is_deleted=False)

    def current_year(self):
        return self.filter(primary_club__in=Club.objects.current_year())

    def for_user_city(self, user=None):
        city_condition = models.Q()

        if user and user.is_authenticated():
            city = get_user_city(user)
            if city:
                city_condition = models.Q(primary_club__city=city) | \
                                 models.Q(primary_club__city="")
        return self.filter(city_condition)

    def for_user_gender(self, user=None):
        gender_condition = models.Q()

        if user and user.is_authenticated():
            gender = get_user_gender(user)
            if gender:
                gender_condition = models.Q(gender=gender) | \
                                   models.Q(gender="")

        return self.filter(gender_condition)

    def for_user_clubs(self, user=None):
        club_condition = models.Q()

        if user and user.is_authenticated():
            user_coordination = get_user_coordination_and_deputyships(user)
            user_clubs = user_coordination | user.memberships.current_year()
            club_condition = models.Q(primary_club__in=user_clubs) | \
                             models.Q(secondary_clubs__in=user_clubs) | \
                             models.Q(review__reviewer_club__in=user_clubs)

        return self.filter(club_condition)

    def done(self):
        activities_end_today_pks = []
        activities_end_today = self.filter(episode__end_date=timezone.now().date())
        for activity in activities_end_today:
            if activity.episode_set.filter(end_date=timezone.now().date(), end_time__gt=timezone.now().time()).exists():
                continue
            activities_end_today_pks.append(activity.pk)
        return self.exclude(episode__end_date__gte=timezone.now().date()) | self.filter(pk__in=activities_end_today_pks)

    def upcoming(self):
        done_activity_pks = self.done().values_list('pk', flat=True)
        return self.exclude(pk__in=done_activity_pks)

    def for_user(self, user=None):
        """
        Return the queryset of activities the user is allowed to see.
        If no user is specified, return only approved activities.
        """
        # If user is not specified, or user is not a coordinator or deputy of any club, return only approved
        # If user is a superuser, return everything
        # If user is a coordinator or deputy, return (a) all the user's club's activities + (b) activities by child
        #   and grandchild clubs that have been approved by the club's direct reviewer child (the first child that
        #   has `can_review=True`) + (c) all activities by clubs that directly submit their activities to this
        #   club + (d) all approved activities

        if not user:
            return self.approved()

        elif user.is_superuser:
            return self.all()

        elif is_coordinator_of_any_club(user) or is_deputy_of_any_club(user):
            clubs = get_user_coordination_and_deputyships(user)
            a = self.filter(primary_club__in=clubs)

            def get_reviewer_children(club):
                """
                Return a list of a club's reviewer children; ie, the clubs whose reviews go up to this club.
                As well as a list of the club's bottom children; ie, children at the bottom of the hierarchy that
                submit their activities to this club.
                """
                reviewer_children = list()
                for child in club.children.all():
                    # If the club can review then add it and move to the next
                    if child.can_review:
                        reviewer_children.append(child)
                    else:
                        # Otherwise, look at the children of the club
                        reviewer_children.extend(get_reviewer_children(child))

                return reviewer_children

            def get_bottom_children(club):
                """
                Return  a list of the club's bottom children; ie, children at the bottom of the hierarchy that
                submit their activities to this club.
                """
                bottom_children = list()
                for child in club.children.all():
                    # If the club is at the bottom of the hierarchy,
                    # then add it and move to the next
                    if child.children.count() == 0:
                        bottom_children.append(child)
                    else:
                        # Otherwise, look at the children of the club
                        bottom_children.extend(get_bottom_children(child))

                return bottom_children

            reviewer_children = set(child for club in clubs for child in get_reviewer_children(club))
            b = self.filter(review__is_approved=True, review__reviewer_club__in=reviewer_children)

            bottom_children = set(child for club in clubs for child in get_bottom_children(club))
            c = self.filter(primary_club__in=bottom_children)

            d = self.approved()

            return (a | b | c | d).filter(is_deleted=False).distinct()

        else:
            return self.approved()

class EpisodeQuerySet(models.QuerySet):
    def upcoming(self):
        # episodes from tomorrow onward +  episodes that are today but later in the day
        return self.filter(start_date__gt=timezone.now().date()) \
             | self.filter(start_date=timezone.now().date(),
                           start_time__gte=timezone.now().time())
