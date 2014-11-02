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
