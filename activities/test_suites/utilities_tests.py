from django.test import TestCase
from accounts.test_utils import create_user
from activities.models import Activity, Review
from activities.test_utils import create_activity
# from activities.utils import Activity.objects.rejected, Activity.objects.pending
#
# from ..utils import Activity.objects.approved


# TODO: modify documentation to include get_rejected and get_pending
class ActivityGetterTests(TestCase):
    """
    Test suite for the get approved activities function.
    """
    # In terms of reviews, an activity can be in one of 16 states
    # In terms of presidency review alone, there are 4 states:
    #  * No presidency review (case 1.1)
    #  * Pending presidency review (case 1.2)
    #  * Rejected presidency review (case 1.3)
    #  * Approved presidency review (case 1.4)
    # As for the DSA (Deanship of Student Affairs) review, the same 4 conditions exist (cases 2.1 through 2.4).
    # Therefore, the overall (theoretical) states are 4 * 4 = 16.
    #
    # In practical terms, not all of these cases exist, since the DSA review only exists
    # when there is a presidency review and that presidency review is approved (case 1.4).
    # This means that the DSA review cases should only be taken into consideration when
    # the presidency review is approved (case 1.4), which reduces the total number of cases from:
    #   1 * 4    (case 1.1) * (2.1 through 2.4)
    # + 1 * 4    (case 1.2) * (2.1 through 2.4)
    # + 1 * 4    (case 1.3) * (2.1 through 2.4)
    # + 1 * 4    (case 1.4) * (2.1 through 2.4)
    # ______
    #   16 cases overall
    #
    # to:
    #
    #   1
    # + 1
    # + 1
    # + 1 * 4    (case 1.4) * (2.1 through 2.4)
    # ______
    #   7 cases overall
    #
    # In any way, an activity should be considered approved only in ONE case out of the 16 (or the 7);
    # and that's when the activity has two approved reviews. (One from the presidency and one from the DSA)
    # On the other hand, it should be considered rejected in 7 cases out of the 16 (2 out of the 7); and that's
    # when either of the reviews gets rejected. Pending activities, finally, are those not approved nor rejected.

    def setUp(self):
        self.user = create_user()
        self.activity = create_activity()

    # case 1.1 * case 2.1
    def test_activity_with_no_reviews(self):
        """
        Test that an activity with no reviews doesn't appear in Activity.objects.approved() nor Activity.objects.rejected()
        but in Activity.objects.pending()
        """
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertNotIn(self.activity, Activity.objects.rejected())
        self.assertIn(self.activity, Activity.objects.pending())

    # case 1.2 * case 2.1
    def test_activity_with_pending_presidency_review(self):
        """
        Test that an activity with only a pending presidency review doesn't appear in
        Activity.objects.approved() nor Activity.objects.rejected() but in Activity.objects.pending()
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=None)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertNotIn(self.activity, Activity.objects.rejected())
        self.assertIn(self.activity, Activity.objects.pending())

    # case 1.3 * case 2.1
    def test_activity_with_rejected_presidency_review(self):
        """
        Test that an activity with only a rejected presidency review doesn't appear in
        Activity.objects.approved() nor Activity.objects.pending() but in Activity.objects.rejected()
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=False)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertIn(self.activity, Activity.objects.rejected())
        self.assertNotIn(self.activity, Activity.objects.pending())

    # case 1.4 * case 2.1
    def test_activity_with_approved_presidency_review_and_no_dsa_review(self):
        """
        Test that an activity with only an approved presidency review doesn't appear in
        Activity.objects.approved() nor rejected but in pending.
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=True)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))
        self.assertQuerysetEqual(self.activity.review_set.filter(review_type='D'),
                                 Review.objects.none())
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertNotIn(self.activity, Activity.objects.rejected())
        self.assertIn(self.activity, Activity.objects.pending())

    # case 1.4 * case 2.2
    def test_activity_with_approved_presidency_review_and_pending_dsa_review(self):
        """
        Test that an activity with an approved presidency review and pending DSA review
        doesn't appear in Activity.objects.approved() nor rejected but in pending.
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=True)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))

        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=None)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertNotIn(self.activity, Activity.objects.rejected())
        self.assertIn(self.activity, Activity.objects.pending())

    # case 1.4 * case 2.3
    def test_activity_with_approved_presidency_review_and_rejected_dsa_review(self):
        """
        Test that an activity with an approved presidency review and rejected DSA review
        doesn't appear in Activity.objects.approved() nor pending but rejected.
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=True)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))

        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=False)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertIn(self.activity, Activity.objects.rejected())
        self.assertNotIn(self.activity, Activity.objects.pending())

    # case 1.4 * case 2.4
    def test_activity_with_approved_presidency_review_and_approved_dsa_review(self):
        """
        Test that an activity with an approved presidency review and an approved DSA review
        DOES appear in Activity.objects.approved() and DOES NOT appear in rejected or pending.
        This is the ONLY case in which the activity is considered to be approved.
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=True)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))

        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=True)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertIn(self.activity, Activity.objects.approved())
        self.assertNotIn(self.activity, Activity.objects.rejected())
        self.assertNotIn(self.activity, Activity.objects.pending())

    ############################################################
    # The remaining cases are rather theoretical and shouldn't #
    # occur in reality, but they may be worth testing as well. #
    ############################################################

    # case 1.1 * case 1.2
    def test_activity_with_no_presidency_review_and_pending_dsa_review(self):
        """
        Test that an activity with no presidency review and pending DSA review
        doesn't appear in Activity.objects.approved()
        """
        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=None)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertNotIn(self.activity, Activity.objects.rejected())
        self.assertIn(self.activity, Activity.objects.pending())

    # case 1.1 * case 1.3
    def test_activity_with_no_presidency_review_and_rejected_dsa_review(self):
        """
        Test that an activity with no presidency review and rejected DSA review
        doesn't appear in Activity.objects.approved()
        """
        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=False)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertIn(self.activity, Activity.objects.rejected())
        self.assertNotIn(self.activity, Activity.objects.pending())

    # case 1.1 * case 1.4
    def test_activity_with_no_presidency_review_and_approved_dsa_review(self):
        """
        Test that an activity with no presidency review and approved DSA review
        doesn't appear in Activity.objects.approved()
        """
        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=True)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertNotIn(self.activity, Activity.objects.rejected())
        self.assertIn(self.activity, Activity.objects.pending())

    # case 1.2 * case 1.2
    def test_activity_with_pending_presidency_review_and_pending_dsa_review(self):
        """
        Test that an activity with a pending presidency review and pending DSA review
        doesn't appear in Activity.objects.approved()
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=None)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))

        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=None)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertNotIn(self.activity, Activity.objects.rejected())
        self.assertIn(self.activity, Activity.objects.pending())

    # case 1.2 * case 1.3
    def test_activity_with_pending_presidency_review_and_rejected_dsa_review(self):
        """
        Test that an activity with a pending presidency review and rejected DSA review
        doesn't appear in Activity.objects.approved()
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=None)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))

        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=False)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertIn(self.activity, Activity.objects.rejected())
        self.assertNotIn(self.activity, Activity.objects.pending())

    # case 1.2 * case 1.4
    def test_activity_with_pending_presidency_review_and_approved_dsa_review(self):
        """
        Test that an activity with a pending presidency review and approved DSA review
        doesn't appear in Activity.objects.approved()
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=None)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))

        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=True)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertNotIn(self.activity, Activity.objects.rejected())
        self.assertIn(self.activity, Activity.objects.pending())

    # case 1.3 * case 1.2
    def test_activity_with_rejected_presidency_review_and_pending_dsa_review(self):
        """
        Test that an activity with a rejected presidency review and pending DSA review
        doesn't appear in Activity.objects.approved()
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=False)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))

        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=None)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertIn(self.activity, Activity.objects.rejected())
        self.assertNotIn(self.activity, Activity.objects.pending())

    # case 1.3 * case 1.3
    def test_activity_with_rejected_presidency_review_and_rejected_dsa_review(self):
        """
        Test that an activity with a rejected presidency review and rejected DSA review
        doesn't appear in Activity.objects.approved()
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=False)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))

        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=False)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertIn(self.activity, Activity.objects.rejected())
        self.assertNotIn(self.activity, Activity.objects.pending())


    # case 1.3 * case 1.4
    def test_activity_with_rejected_presidency_review_and_approved_dsa_review(self):
        """
        Test that an activity with a rejected presidency review and approved DSA review
        doesn't appear in Activity.objects.approved()
        """
        self.p_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='P',
                                                        is_approved=False)
        self.assertIn(self.p_review, self.activity.review_set.filter(review_type='P'))

        self.d_review = self.activity.review_set.create(reviewer=self.user,
                                                        review_type='D',
                                                        is_approved=True)
        self.assertIn(self.d_review, self.activity.review_set.filter(review_type='D'))
        self.assertNotIn(self.activity, Activity.objects.approved())
        self.assertIn(self.activity, Activity.objects.rejected())
        self.assertNotIn(self.activity, Activity.objects.pending())