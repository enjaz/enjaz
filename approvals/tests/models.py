from unittest import TestCase

from approvals.models import RequestThread


class TestRequestThread(TestCase):
    """
    Tests for request threads.
    """

    def test___init__(self):
        """
        Test that request thread only initiates when 1 parameter (and 1 parameter only)
         of `id`, `activity_request`, and `activity` is specified.
        """

        def init_with_no_args():
            request_thread = RequestThread()

        def init_with_many_args():
            request_thread = RequestThread(id=1, activity_request="Some value")

        def init_with_one_arg():
            request_thread = RequestThread(id=1)

        self.assertRaises(AssertionError, init_with_no_args)
        self.assertRaises(AssertionError, init_with_many_args)

        init_with_one_arg()  # This should work properly

    def test_name(self):
        self.fail()


class TestRequestThreadManager(TestCase):
    def test_get(self):
        self.fail()

    def test_filter(self):
        self.fail()

    def test_all(self):
        self.fail()

    def test__get_all_threads(self):
        self.fail()

    def test__get_all_thread_ids(self):
        self.fail()
