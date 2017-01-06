import string
import random

from django.utils import timezone

from core.models import StudentClubYear
import accounts.utils
import clubs.utils


STRING_LENGTH = 6

def generate_random_string(length=STRING_LENGTH):
    look_alike = "O0I1"
    all_chars = string.ascii_uppercase + string.digits
    chars = "".join([char for char in all_chars
                     if not char in look_alike])
    return ''.join(random.choice(chars) for i in range(STRING_LENGTH))

def get_free_random_strings(number):
    # To avoid ImportError
    from niqati.models import Code

    random_strings = []

    while True:
        for i in range(number):
            random_string = generate_random_string()
            random_strings.append(random_string)

        identical_codes = Code.objects.filter(string__in=random_strings)
        if identical_codes.exists():
            identical_strings = [identical_code.string \
                                 for identical_code in identical_codes]
            for identical_string in identical_strings:
                random_strings.pop(identical_string)
            number = len(identical_strings)    
        else:
            break

    return random_strings

def can_claim_niqati(user):
    return not clubs.utils.is_coordinator_of_any_club(user) and \
           not user.is_superuser

def is_niqati_closed(user=None, activity=None):
    if user:
        year = StudentClubYear.objects.get_current()
        city = accounts.utils.get_user_city(user)
    elif activity:
        year = activity.primary_club.year
        city = activity.primary_club.city

    city_code = accounts.utils..get_city_code(city)

    return city_code == 'A' and year.alahsa_niqati_closure_date and \
        timezone.now() >= year.alahsa_niqati_closure_date or \
        city_code == 'J' and year.jeddah_niqati_closure_date and \
        timezone.now() >= year.jeddah_niqati_closure_date or \
        city_code == 'R' and year.riyadh_niqati_closure_date and \
        timezone.now() >= year.riyadh_niqati_closure_date
