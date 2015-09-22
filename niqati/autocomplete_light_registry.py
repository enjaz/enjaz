# -*- coding: utf-8  -*-
import autocomplete_light
from django.contrib.auth.models import User


class UserAutocomplete(autocomplete_light.AutocompleteModelTemplate):
    search_fields=['^email', '^common_profile__ar_first_name',
                   '^common_profile__ar_last_name',
                   '^common_profile__en_first_name',
                   '^common_profile__en_last_name',
                   '^common_profile__student_id',
                   '^common_profile__mobile_number']
    choice_template = 'niqati/autocomplete_choice.html'
    model = User
    attrs = {
         'placeholder': 'أَضف طالبا',
         'data-autocomplete-minimum-characters': 1}
    widget_attrs = {'class': 'modern-style'}
    choices = User.objects.filter(common_profile__is_student=True, coordination__isnull=True, is_active=True)

autocomplete_light.register(UserAutocomplete)
