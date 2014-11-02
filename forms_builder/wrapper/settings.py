from __future__ import unicode_literals

from django.conf import settings

# Use the forms-builder built-in slugs-based urls, or use IDs instead
USE_SLUGS = getattr(settings, "FORMS_BUILDER_USE_SLUGS", True)

# Separate choices by a comma or a user-defined character
CHOICES_SEPARATOR = getattr(settings, "FORMS_BUILDER_CHOICES_SEPARATOR", ",")