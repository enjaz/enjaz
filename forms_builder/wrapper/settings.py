from __future__ import unicode_literals

from django.conf import settings

# Use the forms-builder built-in slugs-based urls, or use IDs instead
USE_SLUGS = getattr(settings, "FORMS_BUILDER_USE_SLUGS", True)