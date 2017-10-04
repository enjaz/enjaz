from __future__ import absolute_import
import rules


@rules.predicate
def is_requestor(user, obj=None):
    pass


@rules.predicate
def is_reviewer(user, obj=None):
    pass


rules.add_perm('approvals.can_submit_activity_creation_request', is_requestor)
rules.add_perm('approvals.can_review_activity_request', is_reviewer)
