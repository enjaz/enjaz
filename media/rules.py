from __future__ import absolute_import
import rules


@rules.predicate
def is_media_center_coordinator(user):
    return user.coordination.current_year().filter(english_name="Media Center").exists()


@rules.predicate
def is_media_center_deputy(user):
    return user.deputyships.current_year().filter(english_name="Media Center").exists()


@rules.predicate
def is_media_center_member(user):
    return user.memberships.current_year().filter(english_name="Media Center").exists()


@rules.predicate
def is_media_representative_of_any_club(user):
    return user.media_representations.current_year().exists()


rules.add_perm(
    "media.can_review_snapchat_reservations",
    is_media_center_coordinator | is_media_center_deputy
)
rules.add_perm(
    "media.can_submit_snapchat_reservations",
    is_media_center_coordinator | is_media_center_deputy | is_media_center_member | is_media_representative_of_any_club
)
