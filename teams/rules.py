from __future__ import absolute_import

import rules


@rules.predicate
def is_supervisor(user):
    return user.is_superuser  # TODO: Change to realistic check; this is just temporary


@rules.predicate
def is_team_leader(user, team):
    return team.leader == user


@rules.predicate
def is_team_member(user, team):
    return team.members.filter(username=user.username).exists()

# This is just an initial list of rules. We'll have to update them as the app unfolds.

rules.add_perm('teams.add_team', is_supervisor)
rules.add_perm('teams.change_team_main_details', is_supervisor)
rules.add_perm('teams.change_team_display_details', is_supervisor | is_team_leader)
rules.add_perm('teams.delete_team', is_supervisor)
rules.add_perm('teams.change_team_members', is_supervisor)

rules.add_perm('teams.change_team_members', is_team_leader)
rules.add_perm('teams.change_team_registration', is_team_leader | is_team_member)

rules.add_perm('teams.view_team_evaluation_summary', is_supervisor)
rules.add_perm('teams.change_members_position', is_team_leader)
