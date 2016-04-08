import string
import random

import clubs.utils

STRING_LENGTH = 6

def get_free_random_strings(number):
    # To avoid ImportError
    from niqati.models import Code

    look_alike = "O0I1"
    all_chars = string.ascii_uppercase + string.digits
    chars = "".join([char for char in all_chars
                     if not char in look_alike])
    random_strings = []

    while True:
        for i in range(number):
            random_string = ''.join(random.choice(chars) for i in range(STRING_LENGTH))
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
