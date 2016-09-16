from django.db import models
from django.utils import timezone
from core.models import StudentClubYear
from accounts.utils import get_user_city, get_user_gender

class BulbQuerySet(models.QuerySet):
    def current_year(self):
        return self.filter()
        year = StudentClubYear.objects.get_current()
        return self.filter(year=year)

    def deleted(self):
        return self.filter(is_deleted=True)

    def undeleted(self):
        return self.filter(is_deleted=False)
    

class NeededBookQuerySet(BulbQuerySet):
    def still_needed(self):
        return self.filter(existing_book__isnull=True)

    def of_user(self, user):
        return self.filter(requester=user)

    def for_user_city(self, user=None):
        city_condition = models.Q()

        if user and user.is_authenticated():
            city = get_user_city(user)
            if city:
                city_condition = models.Q(requester__common_profile__city=city)
        return self.filter(city_condition)

class BookQuerySet(BulbQuerySet):
    def available(self):
        """
        Return a queryset of approved books.
        """
        return self.undeleted().filter(is_available=True)\
                               .exclude(available_until__lte=timezone.now().date())

    def of_user(self, user):
        return self.filter(submitter=user)

    def for_user_city(self, user=None):
        city_condition = models.Q()

        if user and user.is_authenticated():
            city = get_user_city(user)
            if city:
                city_condition = models.Q(submitter__common_profile__city=city)
        return self.filter(city_condition)

class RequestQuerySet(models.QuerySet):
    def current_year(self):
        return self.filter()
        year = StudentClubYear.objects.get_current()
        return self.filter(book__year=year)

    def for_user_city(self, user):
        # Used in indicators
        city_condition = models.Q()
    
        if user and user.is_authenticated():
            city = get_user_city(user)
            if city:
                city_condition = models.Q(requester__common_profile__city=city)
        return self.filter(city_condition)

    def to_user(self, user):
        return self.filter(book__submitter=user)

    def by_user(self, user):
        return self.filter(requester=user)

    def pending(self):
        return self.filter(requester_status='', owner_status='')

    def canceled(self):
        return self.filter(is_canceled=True)

    def successful(self):
        return self.filter(requester_status='D') | \
               self.filter(owner_status='D')

    def disputed(self):
        return (
            self.filter(requester_status='D',
                        owner_status='F') |\
            self.filter(requester_status='F',
                        owner_status='D')
        ).exclude(is_canceled=True)

class PointQuerySet(models.QuerySet):
    def current_year(self):
        return self.filter()
        year = StudentClubYear.objects.get_current()
        return self.filter(year=year)

    def counted(self):
        return self.filter(is_counted=True)

    def giving(self):
        return self.filter(category="G")
    
    def lending(self):
        return self.filter(category="L")

    def count_total_lending(self):
        total = self.current_year().counted().lending().aggregate(total_points=models.Sum('value'))['total_points']
        if total is None:
            return 0
        else:
            return total

    def count_total_giving(self):
        total = self.current_year().counted().giving().aggregate(total_points=models.Sum('value'))['total_points']
        if total is None:
            return 0
        else:
            return total

class GroupQuerySet(BulbQuerySet):
    def unarchived(self):
        return self.filter(is_archived=False)

    def archived(self):
        return self.filter(is_archived=True)

    def for_user_gender(self, user=None):
        gender_condition = models.Q()

        if user and user.is_authenticated():
            gender = get_user_gender(user)
            if gender:
                gender_condition = models.Q(coordinator__common_profile__college__gender=gender, is_limited_by_gender=True) |\
                                   models.Q(is_limited_by_gender=False)
        return self.filter(gender_condition)

    def for_user_city(self, user=None):
        city_condition = models.Q()

        if user and user.is_authenticated():
            city = get_user_city(user)
            if city:
                city_condition = models.Q(coordinator__common_profile__city=city, is_limited_by_city=True) |\
                                 models.Q(is_limited_by_city=False)
        return self.filter(city_condition)

class SessionQuerySet(BulbQuerySet):
    def current_year(self):
        return self.filter()
        year = StudentClubYear.objects.get_current()
        return self.filter(year=year) | self.filter(group__year=year)

    def public(self):
        return self.filter(group__is_private=False)

    def for_user_city(self, user=None):
        city_condition = models.Q()

        if user and user.is_authenticated():
            city = get_user_city(user)
            if city:
                city_condition = models.Q(group__coordinator__common_profile__city=city, group__is_limited_by_city=True) |\
                                 models.Q(group__is_limited_by_city=False) |\
                                 models.Q(group__isnull=True, submitter__common_profile__city=city)
        return self.filter(city_condition)

class MembershipQuerySet(models.QuerySet):
    def current_year(self):
        return self.filter()
        year = StudentClubYear.objects.get_current()
        return self.filter(group__year=year)
 
    def active(self):
        return self.filter(is_active=True)

