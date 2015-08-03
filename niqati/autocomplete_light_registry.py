# -*- coding: utf-8  -*-
import autocomplete_light
from django.contrib.auth.models import User

# This will generate a PersonAutocomplete class
autocomplete_light.register(User,
    search_fields=['^email', '^common_profile__ar_first_name',
                             '^common_profile__ar_last_name',
                             '^common_profile__en_first_name',
                             '^common_profile__en_last_name'],
    attrs={
        'placeholder': 'أَضف طالبا',
        'data-autocomplete-minimum-characters': 1,
    },
    widget_attrs={
        'class': 'modern-style',
    },choices=User.objects.filter(common_profile__is_student=True, coordination__isnull=True))

