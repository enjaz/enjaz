from django.contrib.auth.models import Group
from core.models import StudentClubYear
from clubs.models import Club
from clubs.utils import get_user_coordination_and_deputyships

current_year = StudentClubYear.objects.get_current()

def get_arshidni_club_for_user(user):    
    if user.common_profile:
        city = user.common_profile.city
        # For cities other than Riyadh, we have gender-unspecific
        # Arshidni (yay).
        if city != 'R':
            gender = ''
        else:
            gender = user.common_profile.college.gender
    else:
        # Fall back to the Male Arshidni in Riyadh
        arshidni = Club.objects.get(english_name='Arshidni',
                                    year=current_year, city='R',
                                    gender='M')
    arshidni = Club.objects.get(english_name='Arshidni',
                                year=current_year, city=city,
                                gender=gender)

    return arshidni


def is_arshindi_coordinator_or_deputy(user):
    user_clubs = get_user_coordination_and_deputyships(user)
    return user_clubs.filter(english_name='Arshidni').exists()
