def is_research_committee_member(user):
    return user.memberships.current_year().filter(english_name="Research Committee of the HPC").exists()

def is_organizing_committee_member(user):
    return user.memberships.current_year().filter(english_name="Organizing Committee of the HPC").exists()
