from django.db import models

class RegistrationQuerySet(models.QuerySet):
    def undeleted(self):
        return self.filter(is_deleted=False)

    def male(self):
        return self.filter(nonuser__gender='M') | \
               self.filter(user__common_profile__college__gender='M')

    def female(self):
        return self.filter(nonuser__gender='F') | \
               self.filter(user__common_profile__college__gender='F')

class SessionQuerySet(models.QuerySet):
    # The following methods are obsolete.  They were just used back
    # when Enjaz was linked to the VMA system.
    # def workshops(self):
    #     return self.filter(vma_time_code__isnull=False)
    # def programs(self):
    #     return self.filter(vma_time_code__isnull=True, vma_id__gt=0)
    # def others(self):
    #     return self.filter(vma_time_code__isnull=False, vma_id=0)
    def order_by_date(self):
        return self.order_by('date', 'start_time')

    def onsite(self):
        return self.filter(for_onsite_registration=True)
