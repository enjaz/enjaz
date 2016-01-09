from django.db import models

class RegistrationQuerySet(models.QuerySet):
    def undeleted(self):
        return self.filter(is_deleted=False)

