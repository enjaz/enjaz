from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from model_mommy import mommy

from media.models import Snapchat
from media.views import snapchat_home


class TestSnapchatHome(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.media_center = mommy.make('clubs.Club', english_name="Media Center")
        self.user = mommy.make('auth.User')
        self.media_center.coordinator = self.user
        self.media_center.save()

        self.request = self.factory.get(reverse('media:snapchat_home'))
        self.request.user = self.user

    def test_returns_a_list_of_all_reservations_for_superuser(self):
        self.response = snapchat_home(self.request)

        self.assertQuerysetEqual(self.response.context['snapchat_list'], Snapchat.objects.filter(is_approved=True))

    def test_returns_a_list_of_approved_reservations_according_to_user_city(self):
        self.fail()

    def test_returns_a_list_of_unapproved_reservations_for_media_center_user_according_to_city(self):
        self.fail()

    def test_approves_snapchat_reservation(self):
        self.fail()

    def test_declines_snapchat_reservation(self):
        self.fail()

    def test_cancels_approved_snapchat_reservation(self):
        self.fail()
