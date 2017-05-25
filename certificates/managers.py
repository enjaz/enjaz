from django.db import models
from niqati.utils import generate_random_string

class CertificateQuerySet(models.QuerySet):
    def get_vacant_code(self):
        while True:
            verification_code = generate_random_string(6)
            if not self.filter(verification_code=verification_code).exists():
                break

        return verification_code
