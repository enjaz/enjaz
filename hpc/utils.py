import clubs.utils

def is_research_committee_member(user):
    coordination_and_deputyships = clubs.utils.get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name="Research Committee of the HPC").exists()

def is_organizing_committee_member(user):
    coordination_and_deputyships = clubs.utils.get_user_coordination_and_deputyships(user)
    return coordination_and_deputyships.filter(english_name="Organizing Committee of the HPC").exists()
