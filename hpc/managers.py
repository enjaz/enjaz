from django.db import models

class RegistrationQuerySet(models.QuerySet):
    def undeleted(self):
        return self.filter(is_deleted=False)

class SessionQuerySet(models.QuerySet):
    def workshops(self):
        return self.filter(vma_time_code__isnull=False)
    def programs(self):
        return self.filter(vma_time_code__isnull=True, vma_id__gt=0)
    def others(self):
        return self.filter(vma_time_code__isnull=False, vma_id=0)
