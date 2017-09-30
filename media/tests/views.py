# coding=utf-8
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from model_mommy import mommy

from media.views import snapchat_home


class TestSnapchatHome(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.current_year = mommy.make('core.StudentClubYear')

        # Riyadh
        self.riyadh_coordinator = mommy.make('auth.User', common_profile__city=u"الرياض")
        self.riyadh_deputy = mommy.make('auth.User', common_profile__city=u"الرياض")
        self.riyadh_member = mommy.make('auth.User', common_profile__city=u"الرياض")
        self.riyadh_representative = mommy.make('auth.User', common_profile__city=u"الرياض")

        self.riyadh_media_center = mommy.make(
            'clubs.Club',
            english_name="Media Center",
            city=u"الرياض",
            year=self.current_year,
        )

        self.riyadh_media_center.coordinator = self.riyadh_coordinator
        self.riyadh_media_center.deputies.add(self.riyadh_deputy)
        self.riyadh_media_center.members.add(self.riyadh_member)
        self.riyadh_media_center.save()

        self.riyadh_club = mommy.make(
            'clubs.Club',
            city=u"الرياض",
            year=self.current_year,
        )
        self.riyadh_club.media_representatives.add(self.riyadh_representative)
        self.riyadh_club.save()

        self.riyadh_reservations = [
            mommy.make('media.Snapchat', club__city=u"الرياض", club__year=self.current_year, is_approved=None),  # Unreviewed reservation
            mommy.make('media.Snapchat', club__city=u"الرياض", club__year=self.current_year, is_approved=False),  # Declined reservation
            mommy.make('media.Snapchat', club__city=u"الرياض", club__year=self.current_year, is_approved=True),  # Approved reservation
        ]

        # Jeddah
        self.jeddah_coordinator = mommy.make('auth.User', common_profile__city=u"جدة")
        self.jeddah_deputy = mommy.make('auth.User', common_profile__city=u"جدة")
        self.jeddah_member = mommy.make('auth.User', common_profile__city=u"جدة")
        self.jeddah_representative = mommy.make('auth.User', common_profile__city=u"جدة")


        self.jeddah_media_center = mommy.make(
            'clubs.Club',
            english_name="Media Center",
            city=u"جدة",
            year=self.current_year,
        )

        self.jeddah_media_center.coordinator = self.jeddah_coordinator
        self.jeddah_media_center.deputies.add(self.jeddah_deputy)
        self.jeddah_media_center.members.add(self.jeddah_member)
        self.jeddah_media_center.save()

        self.jeddah_club = mommy.make(
            'clubs.Club',
            city=u"جدة",
            year=self.current_year,
        )
        self.jeddah_club.media_representatives.add(self.jeddah_representative)
        self.jeddah_club.save()

        self.jeddah_reservations = [
            mommy.make('media.Snapchat', club__city=u"جدة", club__year=self.current_year, is_approved=None),  # Unreviewed reservation
            mommy.make('media.Snapchat', club__city=u"جدة", club__year=self.current_year, is_approved=False),  # Declined reservation
            mommy.make('media.Snapchat', club__city=u"جدة", club__year=self.current_year, is_approved=True),  # Approved reservation
        ]

        self.request = self.factory.get(reverse('media:snapchat_home'))

    def test_returns_a_list_of_all_approved_and_pending_reservations_for_superuser(self):
        self.superuser = mommy.make('auth.User', is_superuser=True)

        self.request.user = self.superuser
        self.response = snapchat_home(self.request)

        self.assertEqual(self.response.status_code, 200)

        self.assertContains(self.response, self.riyadh_reservations[0].club.name)
        self.assertContains(self.response, self.riyadh_reservations[2].club.name)
        self.assertContains(self.response, self.jeddah_reservations[0].club.name)
        self.assertContains(self.response, self.jeddah_reservations[2].club.name)

    def test_returns_a_list_of_city_specific_approved_and_pending_reservations_for_media_center_team(self):
        for user in [self.riyadh_coordinator, self.riyadh_deputy, self.riyadh_member]:
            self.request.user = user
            self.response = snapchat_home(self.request)

            self.assertEqual(self.response.status_code, 200)

            self.assertContains(self.response, self.riyadh_reservations[0].club.name)
            self.assertContains(self.response, self.riyadh_reservations[2].club.name)
            self.assertNotContains(self.response, self.jeddah_reservations[0].club.name)
            self.assertNotContains(self.response, self.jeddah_reservations[2].club.name)

    def test_returns_a_list_of_city_specific_approved_reservations_for_media_representative(self):
        self.request.user = self.riyadh_representative
        self.response = snapchat_home(self.request)

        self.assertContains(self.response, self.riyadh_reservations[2].club.name)
        self.assertNotContains(self.response, self.riyadh_reservations[0].club.name)
        self.assertNotContains(self.response, self.jeddah_reservations[0].club.name)
        self.assertNotContains(self.response, self.jeddah_reservations[2].club.name)

    # def test_returns_a_list_of_club_specific_pending_reservations_for_media_representative(self):
    #     self.riyadh_club_reservation = mommy.make('media.Snapchat', club=self.riyadh_club, is_approved=None)
    #
    #     self.request.user = self.riyadh_representative
    #     self.response = snapchat_home(self.request)
    #
    #     self.assertContains(self.response, self.riyadh_club_reservation.club.name)

    def test_approves_pending_snapchat_reservation(self):
        self.request = self.factory.post(reverse('media:snapchat_home'), {'approve': self.riyadh_reservations[0].id})
        self.request.user = self.riyadh_coordinator
        self.response = snapchat_home(self.request)

        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, u"تم قبول طلب {}".format(self.riyadh_reservations[0].club.name))

        self.riyadh_reservations[0].refresh_from_db()

        self.assertTrue(self.riyadh_reservations[0].is_approved)

    def test_declines_pending_snapchat_reservation(self):
        self.request = self.factory.post(reverse('media:snapchat_home'), {'disapprove': self.riyadh_reservations[0].id})
        self.request.user = self.riyadh_coordinator
        self.response = snapchat_home(self.request)

        self.assertEqual(self.response.status_code, 200)
        # self.assertContains(self.response, u"تم رفض طلب {}".format(self.riyadh_reservations[0].club.name))

        self.riyadh_reservations[0].refresh_from_db()

        self.assertFalse(self.riyadh_reservations[0].is_approved)

    def test_cancels_approved_snapchat_reservation(self):
        self.request = self.factory.post(reverse('media:snapchat_home'), {'cancel': self.riyadh_reservations[2].id})

        self.request.user = self.riyadh_coordinator
        self.response = snapchat_home(self.request)

        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, u"تم إلغاء طلب {}".format(self.riyadh_reservations[2].club.name))

        self.riyadh_reservations[2].refresh_from_db()

        self.assertIsNone(self.riyadh_reservations[2].is_approved)
