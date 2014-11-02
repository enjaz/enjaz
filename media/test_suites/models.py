import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from accounts.test_utils import create_user
from media.models import Poll, PollResponse, HUNDRED_SAYS, WHAT_IF
from media.test_utils import create_poll, create_poll_response


class PollManagerTests(TestCase):
    def setUp(self):
        self.old_poll = create_poll(poll_type=HUNDRED_SAYS,
                                    open_date=(timezone.now() + datetime.timedelta(days=-30)),
                                    close_date=(timezone.now() + datetime.timedelta(days=-15)))
        self.current_poll = create_poll(poll_type=HUNDRED_SAYS,
                                    open_date=(timezone.now() + datetime.timedelta(days=-5)),
                                    close_date=(timezone.now() + datetime.timedelta(days=5)))
        self.upcoming_poll = create_poll(poll_type=HUNDRED_SAYS,
                                    open_date=(timezone.now() + datetime.timedelta(days=5)),
                                    close_date=(timezone.now() + datetime.timedelta(days=10)))

    def test_active(self):
        """
        Active polls are those that satisfy: open date [before] now [before] close date
        """
        self.assertNotIn(self.old_poll, Poll.objects.active())
        self.assertIn(self.current_poll, Poll.objects.active())
        self.assertNotIn(self.upcoming_poll, Poll.objects.active())

    def test_previous(self):
        """
        Previous polls are those which satisfy: close date [before] now
        """
        self.assertIn(self.old_poll, Poll.objects.previous())
        self.assertNotIn(self.current_poll, Poll.objects.previous())
        self.assertNotIn(self.upcoming_poll, Poll.objects.previous())

class PollModelTests(TestCase):
    def test_choice_restrictions(self):
        """
        hundred-says polls should have choices
        what-if polls shouldn't
        """
        # A What-if poll with no choices -> no problem
        self.what_if_poll = Poll(poll_type=WHAT_IF, title="TEST", text="TEST", open_date=timezone.now(),
                                 close_date=timezone.now() + datetime.timedelta(days=7),
                                 choices="", creator=create_user())
        self.assertIsNone(self.what_if_poll.clean())  # Just to make sure no ValidationError is raised

        # A What-if poll with choices -> problem
        self.what_if_poll.choices = "ABC/DEF/GHI"
        self.assertRaises(ValidationError, self.what_if_poll.clean)

        # A hundred-says poll with choices -> no problem
        self.hundred_says_poll = Poll(poll_type=HUNDRED_SAYS, title="TEST", text="TEST", open_date=timezone.now(),
                                      close_date=timezone.now() + datetime.timedelta(days=7),
                                      choices="ABC/DEF/GHI", creator=create_user())
        self.assertIsNone(self.hundred_says_poll.clean())  # Just to make sure no ValidationError is raised

        # A hundred-says poll with no choices -> problem
        self.hundred_says_poll.choices = ""
        self.assertRaises(ValidationError, self.hundred_says_poll.clean)

    def test_choice_update(self):
        """
        If choices of a poll are updated, all responses should be updated to correspond to the change.
        """
        self.poll = create_poll(HUNDRED_SAYS, choices=["ABC", "DEF", "GHI"])
        self.response1 = create_poll_response(poll=self.poll, choice="ABC")
        self.response2 = create_poll_response(poll=self.poll, choice="ABC")
        self.response3 = create_poll_response(poll=self.poll, choice="DEF")
        self.response4 = create_poll_response(poll=self.poll, choice="GHI")

        # For some reason, update the choices of the poll
        self.poll.choices = "ABC123/DEF/GHI"
        self.poll.save()

        # Check that the responses containing the edited choice have been updated
        self.assertEqual(PollResponse.objects.get(pk=self.response1.pk).choice, "ABC123")
        self.assertEqual(PollResponse.objects.get(pk=self.response2.pk).choice, "ABC123")

        # Other responses shouldn't be affected
        self.assertEqual(PollResponse.objects.get(pk=self.response3.pk).choice, "DEF")
        self.assertEqual(PollResponse.objects.get(pk=self.response4.pk).choice, "GHI")

        # Q: What if a choice is added/deleted?

class PollResponseTests(TestCase):
    def setUp(self):
        pass

    def test_choice_restrictions(self):
        """
        response to hundred-says polls should have a choice selected
        response to what-if polls shouldn't
        """
        pass