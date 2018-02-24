import clubs.utils
from models import StudentApplication
def is_matchingProgram_coordinator_or_member(user):
    coordination_and_deputyships = clubs.utils.get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name='MatchingProgram').exists()


def is_new_application(user, pk):
    applications = StudentApplication.objects.filter(research_id=pk)
    for i in applications:
        if i.user == user:
            return False
    return True


