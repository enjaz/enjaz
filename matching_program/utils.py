import clubs.utils
from clubs.models import Club
import json
from models import StudentApplication

def is_matchingProgram_coordinator_or_member(user):
    club = Club.objects.get(name="matching_program")
    coordination_and_member = clubs.utils.is_coordinator_or_member(club, user)
    return coordination_and_member

def is_matchingProgram_coordinator(user):
    club = Club.objects.get(name="matching_program")
    coordinator = clubs.utils.is_coordinator(club, user)
    return coordinator

def is_new_application(user, pk):
    applications = StudentApplication.objects.filter(research_id=pk)
    for i in applications:
        if i.user == user:
            return False
    return True


