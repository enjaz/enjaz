from django.db import models
from django.db.models.aggregates import Count
from clubs.utils import is_coordinator_of_any_club, is_deputy_of_any_club, get_user_clubs, \
    get_user_coordination_and_deputyships


class ActivityManager(models.Manager):
    """
    Custom manager for Activity model with custom querysets
    for approved, pending, and rejected activities.
    """
    def get_queryset(self):
        """
        TODO: Exclude delete activities.
        TODO: Exclude but the current year's activities.
        """
        return super(ActivityManager, self).get_queryset()

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

        activities = self.filter(is_deleted=False)
        approved_activities = filter(lambda activity: activity.is_approved(), activities)
        approved_pks = [activity.pk for activity in approved_activities]

        return self.filter(pk__in=approved_pks)

    def rejected(self):
        """
        Return a queryset of rejected activities.
        """
        # A rejected activity is one which:
        # (1) has at least 1 review
        # (2) has any of its reviews rejected
        return self.filter(is_deleted=False).annotate(review_count=Count("review")).filter(review_count__gte=1, review__is_approved=False)

    def pending(self):
        """
        Return a queryset of pending activities.
        """
        # A pending activity is one that's not approved or rejected

        # The following is dirty way of dealing with query sets, but this is the only way given the deep complexity
        # of this query

        # WARNING: lengthy run-time; not lazy

        pending_activities = filter(lambda activity: activity.is_approved() is None, self.filter(is_deleted=False))
        pending_pks = [activity.pk for activity in pending_activities]

        return self.filter(pk__in=pending_pks)

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
