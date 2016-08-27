from django.db import models
from accounts.utils import get_user_city, get_user_gender
from core.models import StudentClubYear


class ClubQuerySet(models.QuerySet):
    """
    Custom manager for Activity model with custom querysets
    for approved, pending, and rejected activities.
    """
    def visible(self):
        return self.filter(visible=True)

    def current_year(self):
        current_year = StudentClubYear.objects.get_current()
        return self.filter(models.Q(year=current_year) | models.Q(year__isnull=True))

    def for_user_city(self, user=None):
        city_condition = models.Q()

        if user:
            city = get_user_city(user)
            if city:
                city_condition = models.Q(city=city) | \
                                 models.Q(city="")
        return self.filter(city_condition)

    def for_user_gender(self, user=None):
        gender_condition = models.Q()

        if user:
            gender = get_user_gender(user)
            if gender:
                gender_condition = models.Q(gender=gender) | \
                                   models.Q(gender="")
        return self.filter(gender_condition)

    def reviewing_parents(self, club):
        reviewing_parent_pks = []
        new_parent = club.parent

        while new_parent:
            if new_parent.can_review:
                reviewing_parent_pks.append(new_parent.pk)

            new_parent = new_parent.parent

        return self.filter(pk__in=reviewing_parent_pks)

    def activity_reviewing_parents(self, activity):
        if activity.chosen_reviewer_club:
            chosen_reviewer_query = self.filter(pk=activity.chosen_reviewer_club.pk)
        else:
            chosen_reviewer_query = self.none()

        reviewing_parent_pks = []
        new_parent = activity.primary_club.parent

        while new_parent:
            if new_parent.can_review:
                reviewing_parent_pks.append(new_parent.pk)

            new_parent = new_parent.parent

        return chosen_reviewer_query | self.filter(pk__in=reviewing_parent_pks)

    def club_assessing_parents(self, club):
        assessing_parent_pks = []
        new_parent = club.parent

        while new_parent:
            if new_parent.can_assess:
                assessing_parent_pks.append(new_parent.pk)

            new_parent = new_parent.parent

        return self.filter(pk__in=assessing_parent_pks)

    def niqati_reviewing_parents(self, order):
        reviewing_parent_pks = []
        
        new_parent = order.episode.activity.primary_club
        while new_parent:
            if new_parent.can_review_niqati:
                reviewing_parent_pks.append(new_parent.pk)

            new_parent = new_parent.parent

        return self.filter(pk__in=reviewing_parent_pks)
