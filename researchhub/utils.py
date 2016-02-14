import clubs.utils

def is_researchhub_coordinator_or_member(user):
    coordination_and_deputyships = clubs.utils.get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name='ResearchHub').exists()

def is_supervisor(user):
    return bool(user.supervisor)

def can_edit_skill(user, skill):
    if skill.is_deleted:
        return False
    elif user.is_superuser or \
         is_researchhub_coordinator_or_member(user) or \
         skill.user == user:
        return True
    else:
        return False

def can_edit_project(user, project):
    if project.is_deleted:
        return False
    elif user.is_superuser or \
         is_researchhub_coordinator_or_member(user) or \
         project.submitter == user:
        return True
    else:
        return False

def can_edit_supervisor(user, supervisor):
    if supervisor.is_deleted:
        return False
    elif user.is_superuser or \
         is_researchhub_coordinator_or_member(user) or \
         supervisor.user == user:
        return True
    else:
        return False
