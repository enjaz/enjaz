from django.contrib import admin
from certificates.models import CertificateTemplate, CertificateRequest, Certificate

admin.site.register(Certificate)
admin.site.register(CertificateRequest)
admin.site.register(CertificateTemplate)
