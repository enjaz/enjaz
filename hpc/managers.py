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
    def workshops(self):
        return self.filter(vma_time_code__isnull=False)
    def programs(self):
        return self.filter(vma_time_code__isnull=True, vma_id__gt=0)
    def others(self):
        return self.filter(vma_time_code__isnull=False, vma_id=0)
    def onsite(self):
        return self.filter(for_onsite_registration=True)
