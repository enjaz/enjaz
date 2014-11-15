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
        self.active_poll = create_poll(poll_type=HUNDRED_SAYS,
                                    open_date=(timezone.now() + datetime.timedelta(days=-5)),
                                    close_date=(timezone.now() + datetime.timedelta(days=5)))
        self.active_poll_start_on_same_day = create_poll(poll_type=HUNDRED_SAYS,
                                    open_date=(timezone.now() + datetime.timedelta(minutes=-30)),
                                    close_date=(timezone.now() + datetime.timedelta(days=10)))
        self.active_poll_end_on_same_day = create_poll(poll_type=HUNDRED_SAYS,
                                    open_date=(timezone.now() + datetime.timedelta(days=-10)),
                                    close_date=(timezone.now() + datetime.timedelta(minutes=30)))
        self.upcoming_poll = create_poll(poll_type=HUNDRED_SAYS,
                                    open_date=(timezone.now() + datetime.timedelta(days=5)),
                                    close_date=(timezone.now() + datetime.timedelta(days=10)))

    def test_active(self):
        """
        Active polls are those that satisfy: open date [before] now [before] close date
        """
        self.assertNotIn(self.old_poll, Poll.objects.active())
        self.assertIn(self.active_poll, Poll.objects.active())
        self.assertIn(self.active_poll_start_on_same_day, Poll.objects.active())
        self.assertIn(self.active_poll_end_on_same_day, Poll.objects.active())
        self.assertNotIn(self.upcoming_poll, Poll.objects.active())

    def test_past(self):
        """
        Previous polls are those which satisfy: close date [before] now
        """
        self.assertIn(self.old_poll, Poll.objects.past())
        self.assertNotIn(self.active_poll, Poll.objects.past())
        self.assertNotIn(self.upcoming_poll, Poll.objects.past())

    def test_upcoming(self):
        """
        Upcoming polls are those which satisfy: now [before] open date
        """
        self.assertNotIn(self.old_poll, Poll.objects.upcoming())
        self.assertNotIn(self.active_poll, Poll.objects.upcoming())
        self.assertIn(self.upcoming_poll, Poll.objects.upcoming())
