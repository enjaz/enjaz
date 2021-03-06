# coding=utf-8
from datetime import date, time

from django.core.urlresolvers import reverse
from django.test import TestCase
from model_mommy import mommy
from post_office.models import Email

from media.models import SnapchatReservation


class TestUserMixin(object):
    password = '123'

    def create_user_and_set_password(self, *args, **kwargs):
        user = mommy.make('auth.User', *args, **kwargs)
        user.set_password(self.password)
        user.save()
        return user


class TestSubmitFollowUpReport(TestUserMixin, TestCase):
    def setUp(self):
        self.user = self.create_user_and_set_password()
        self.client.login(username=self.user.username, password=self.password)
        self.episode = mommy.make('activities.Episode', activity__primary_club=mommy.make('clubs.Club'))
        self.episode.activity.primary_club.media_representatives.add(self.user)

    def test_submit_follow_up_report(self):
        response = self.client.get(reverse('media:submit_report', args=(self.episode.id,)))
        self.assertEqual(response.status_code, 200)


class TestEditFollowUpReport(TestUserMixin, TestCase):
    def setUp(self):
        self.user = self.create_user_and_set_password()
        self.client.login(username=self.user.username, password=self.password)
        self.episode = mommy.make('activities.Episode', activity__primary_club=mommy.make('clubs.Club'))
        self.episode.activity.primary_club.media_representatives.add(self.user)
        mommy.make('media.FollowUpReport', episode=self.episode)

    def test_edit_follow_up_report(self):
        response = self.client.get(reverse('media:edit_report', args=(self.episode.id,)))
        self.assertEqual(response.status_code, 200)


class TestSubmitEmployeeReport(TestUserMixin, TestCase):
    def setUp(self):
        self.user = self.create_user_and_set_password()
        self.client.login(username=self.user.username, password=self.password)
        self.episode = mommy.make('activities.Episode', activity__primary_club__employee=self.user)

    def test_submit_employee_report(self):
        response = self.client.get(reverse('media:submit_employee_report', args=(self.episode.id,)))
        self.assertEqual(response.status_code, 200)

    def test_employee_report_page_does_not_show_save_as_draft_button(self):
        response = self.client.get(reverse('media:submit_employee_report', args=(self.episode.id,)))
        self.assertNotContains(response, u"احفظ كمسودة فقط")


class TestEditEmployeeReport(TestUserMixin, TestCase):
    def setUp(self):
        self.user = self.create_user_and_set_password()
        self.client.login(username=self.user.username, password=self.password)
        self.episode = mommy.make('activities.Episode', activity__primary_club__employee=self.user)
        self.employee_report = mommy.make('media.EmployeeReport', episode=self.episode)

    def test_edit_employee_report(self):
        response = self.client.get(reverse('media:edit_employee_report', args=(self.employee_report.id,)))
        self.assertEqual(response.status_code, 200)

    def test_employee_report_page_does_not_show_save_as_draft_button(self):
        response = self.client.get(reverse('media:edit_employee_report', args=(self.employee_report.id,)))
        self.assertNotContains(response, u"احفظ كمسودة فقط")




class TestSnapchatHome(TestUserMixin, TestCase):
    fixtures = ['default_emailtemplates.json']

    def setUp(self):
        self.current_year = mommy.make('core.StudentClubYear')

        # Riyadh
        self.riyadh_coordinator = self.create_user_and_set_password(common_profile__city=u"الرياض")
        self.riyadh_deputy = self.create_user_and_set_password(common_profile__city=u"الرياض")
        self.riyadh_member = self.create_user_and_set_password(common_profile__city=u"الرياض")
        self.riyadh_representative = self.create_user_and_set_password(common_profile__city=u"الرياض")

        self.riyadh_media_center = mommy.make(
            'clubs.Club',
            english_name="Media Center",
            city=u"الرياض",
            year=self.current_year,
            gender="M",
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
            mommy.make('media.SnapchatReservation', club__city=u"الرياض", club__year=self.current_year,
                       club__coordinator__email="example@example.com", is_approved=None),  # Unreviewed reservation
            mommy.make('media.SnapchatReservation', club__city=u"الرياض", club__year=self.current_year,
                       club__coordinator__email="example@example.com", is_approved=False),  # Declined reservation
            mommy.make('media.SnapchatReservation', club__city=u"الرياض", club__year=self.current_year,
                       club__coordinator__email="example@example.com", is_approved=True),  # Approved reservation
        ]

        # Jeddah
        self.jeddah_coordinator = self.create_user_and_set_password(common_profile__city=u"جدة")
        self.jeddah_deputy = self.create_user_and_set_password(common_profile__city=u"جدة")
        self.jeddah_member = self.create_user_and_set_password(common_profile__city=u"جدة")
        self.jeddah_representative = self.create_user_and_set_password(common_profile__city=u"جدة")

        self.jeddah_media_center = mommy.make(
            'clubs.Club',
            english_name="Media Center",
            city=u"جدة",
            year=self.current_year,
            gender="M",
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
            mommy.make('media.SnapchatReservation', club__city=u"جدة", club__year=self.current_year,
                       club__coordinator__email="example@example.com", is_approved=None),
            # Unreviewed reservation
            mommy.make('media.SnapchatReservation', club__city=u"جدة", club__year=self.current_year,
                       club__coordinator__email="example@example.com", is_approved=False),
            # Declined reservation
            mommy.make('media.SnapchatReservation', club__city=u"جدة", club__year=self.current_year,
                       club__coordinator__email="example@example.com", is_approved=True),
            # Approved reservation
        ]

    def test_returns_a_list_of_all_approved_and_pending_reservations_for_superuser(self):
        self.superuser = self.create_user_and_set_password(is_superuser=True)

        self.client.login(username=self.superuser.username, password=self.password)
        self.response = self.client.get(reverse('media:snapchat_home'))

        self.assertEqual(self.response.status_code, 200)

        self.assertContains(self.response, self.riyadh_reservations[0].club.name)
        self.assertContains(self.response, self.riyadh_reservations[2].club.name)
        self.assertContains(self.response, self.jeddah_reservations[0].club.name)
        self.assertContains(self.response, self.jeddah_reservations[2].club.name)

    def test_returns_a_list_of_city_specific_approved_and_pending_reservations_for_media_center_team(self):
        for user in [self.riyadh_coordinator, self.riyadh_deputy, self.riyadh_member]:
            self.client.login(username=user.username, password=self.password)
            self.response = self.client.get(reverse('media:snapchat_home'))

            self.assertEqual(self.response.status_code, 200)

            self.assertContains(self.response, self.riyadh_reservations[0].club.name)
            self.assertContains(self.response, self.riyadh_reservations[2].club.name)
            self.assertNotContains(self.response, self.jeddah_reservations[0].club.name)
            self.assertNotContains(self.response, self.jeddah_reservations[2].club.name)

    def test_returns_a_list_of_city_specific_approved_reservations_for_media_representative(self):
        self.client.login(username=self.riyadh_representative.username, password=self.password)
        self.response = self.client.get(reverse('media:snapchat_home'))

        self.assertContains(self.response, self.riyadh_reservations[2].club.name)
        self.assertNotContains(self.response, self.riyadh_reservations[0].club.name)
        self.assertNotContains(self.response, self.jeddah_reservations[0].club.name)
        self.assertNotContains(self.response, self.jeddah_reservations[2].club.name)

    # def test_returns_a_list_of_club_specific_pending_reservations_for_media_representative(self):
    #     self.riyadh_club_reservation = mommy.make('media.SnapchatReservation', club=self.riyadh_club, is_approved=None)
    #
    #     self.request.user = self.riyadh_representative
    #     self.response = snapchat_home(self.request)
    #
    #     self.assertContains(self.response, self.riyadh_club_reservation.club.name)

    def test_approves_pending_snapchat_reservation(self):
        self.client.login(username=self.riyadh_coordinator.username, password=self.password)
        self.response = self.client.post(reverse('media:snapchat_home'), {'approve': self.riyadh_reservations[0].id})

        self.assertEqual(self.response.status_code, 302)
        # self.assertContains(self.response, u"تم قبول طلب {}".format(self.riyadh_reservations[0].club.name))

        self.riyadh_reservations[0].refresh_from_db()

        self.assertTrue(self.riyadh_reservations[0].is_approved)

    def test_sends_email_upon_approval_of_pending_snapchat_reservation(self):
        self.client.login(username=self.riyadh_coordinator.username, password=self.password)
        self.response = self.client.post(reverse('media:snapchat_home'), {'approve': self.riyadh_reservations[0].id})

        self.assertEqual(Email.objects.count(), 1)
        self.assertEqual(Email.objects.last().to, [self.riyadh_reservations[0].club.coordinator.email])

    def test_declines_pending_snapchat_reservation(self):
        self.client.login(username=self.riyadh_coordinator.username, password=self.password)
        self.response = self.client.post(reverse('media:snapchat_home'), {'disapprove': self.riyadh_reservations[0].id})

        self.assertEqual(self.response.status_code, 302)
        # self.assertContains(self.response, u"تم رفض طلب {}".format(self.riyadh_reservations[0].club.name))

        self.riyadh_reservations[0].refresh_from_db()

        self.assertFalse(self.riyadh_reservations[0].is_approved)

    def test_sends_email_upon_decline_of_pending_snapchat_reservation(self):
        self.client.login(username=self.riyadh_coordinator.username, password=self.password)
        self.response = self.client.post(reverse('media:snapchat_home'),
                                         {'disapprove': self.riyadh_reservations[0].id})

        self.assertEqual(Email.objects.count(), 1)
        self.assertEqual(Email.objects.last().to, [self.riyadh_reservations[0].club.coordinator.email])

    def test_cancels_approved_snapchat_reservation(self):
        self.client.login(username=self.riyadh_coordinator.username, password=self.password)
        self.response = self.client.post(reverse('media:snapchat_home'), {'cancel': self.riyadh_reservations[2].id})

        self.assertEqual(self.response.status_code, 302)
        # self.assertContains(self.response, u"تم إلغاء طلب {}".format(self.riyadh_reservations[2].club.name))

        self.riyadh_reservations[2].refresh_from_db()

        self.assertIsNone(self.riyadh_reservations[2].is_approved)

    def test_sends_email_upon_revoke_of_approved_snapchat_reservation(self):
        self.client.login(username=self.riyadh_coordinator.username, password=self.password)
        self.response = self.client.post(reverse('media:snapchat_home'),
                                         {'cancel': self.riyadh_reservations[2].id})

        self.assertEqual(Email.objects.count(), 1)
        self.assertEqual(Email.objects.last().to, [self.riyadh_reservations[2].club.coordinator.email])


class TestSnapchatAdd(TestUserMixin, TestCase):
    fixtures = ['default_emailtemplates.json']

    def setUp(self):
        self.current_year = mommy.make('core.StudentClubYear')

        # Riyadh
        self.riyadh_coordinator = self.create_user_and_set_password(common_profile__city=u"الرياض", email="riyadh@example.com")
        self.riyadh_deputy = self.create_user_and_set_password(common_profile__city=u"الرياض")
        self.riyadh_member = self.create_user_and_set_password(common_profile__city=u"الرياض")
        self.riyadh_representative = self.create_user_and_set_password(common_profile__city=u"الرياض")

        self.riyadh_media_center = mommy.make(
            'clubs.Club',
            english_name="Media Center",
            city=u"الرياض",
            year=self.current_year,
            gender="M",
        )

        self.riyadh_media_center.coordinator = self.riyadh_coordinator
        self.riyadh_media_center.deputies.add(self.riyadh_deputy)
        self.riyadh_media_center.members.add(self.riyadh_member)
        self.riyadh_media_center.save()

        self.riyadh_clubs = mommy.make(
            'clubs.Club',
            city=u"الرياض",
            year=self.current_year,
            _quantity=10,
        )
        self.riyadh_clubs[0].media_representatives.add(self.riyadh_representative)
        self.riyadh_clubs[0].save()

        # Jeddah
        self.jeddah_coordinator = self.create_user_and_set_password(common_profile__city=u"جدة", email="jeddah@example.com")
        self.jeddah_deputy = self.create_user_and_set_password(common_profile__city=u"جدة")
        self.jeddah_member = self.create_user_and_set_password(common_profile__city=u"جدة")
        self.jeddah_representative = self.create_user_and_set_password(common_profile__city=u"جدة")

        self.jeddah_media_center = mommy.make(
            'clubs.Club',
            english_name="Media Center",
            city=u"جدة",
            year=self.current_year,
            gender="M",
        )

        self.jeddah_media_center.coordinator = self.jeddah_coordinator
        self.jeddah_media_center.deputies.add(self.jeddah_deputy)
        self.jeddah_media_center.members.add(self.jeddah_member)
        self.jeddah_media_center.save()

        self.jeddah_clubs = mommy.make(
            'clubs.Club',
            city=u"جدة",
            year=self.current_year,
            _quantity=10,
        )
        self.jeddah_clubs[0].media_representatives.add(self.jeddah_representative)
        self.jeddah_clubs[0].save()

    def test_shows_a_list_of_all_clubs_for_superuser(self):
        self.superuser = self.create_user_and_set_password(is_superuser=True)

        self.client.login(username=self.superuser.username, password=self.password)
        self.response = self.client.get(reverse('media:snapchat_add'))

        for club in self.riyadh_clubs + self.jeddah_clubs:
            self.assertContains(self.response, club.name)

    def test_shows_a_list_of_city_specific_clubs_for_media_center_team_and_media_representative(self):
        for user in [self.riyadh_coordinator, self.riyadh_deputy, self.riyadh_member, self.riyadh_representative]:
            self.client.login(username=user.username, password=self.password)
            self.response = self.client.get(reverse('media:snapchat_add'))

            for club in self.riyadh_clubs:
                self.assertContains(self.response, club.name)

            for club in self.jeddah_clubs:
                self.assertNotContains(self.response, club.name)

    def test_creates_a_snapchat_reservation(self):
        self.client.login(username=self.riyadh_representative.username, password=self.password)
        self.response = self.client.post(
            reverse('media:snapchat_add'),
            {
                'club': self.riyadh_clubs[0].id,
                'date': "10/10/2017",
                'start_time': "12:00 PM",
                'end_time': "1:00 PM",
            }
        )

        self.assertEqual(SnapchatReservation.objects.count(), 1)

        created_reservation = SnapchatReservation.objects.get()
        self.assertEqual(created_reservation.club, self.riyadh_clubs[0])
        self.assertEqual(created_reservation.date, date(2017, 10, 10))
        self.assertEqual(created_reservation.start_time, time(12, 0))
        self.assertEqual(created_reservation.end_time, time(13, 0))

    def test_sends_an_email_to_city_appropriate_media_center_up_snapchat_reservation(self):
        self.client.login(username=self.jeddah_representative.username, password=self.password)
        self.response = self.client.post(
            reverse('media:snapchat_add'),
            {
                'club': self.jeddah_clubs[0].id,
                'date': "10/10/2017",
                'start_time': "12:00 PM",
                'end_time': "1:00 PM",
            }
        )

        self.assertEqual(Email.objects.count(), 1)
        self.assertEqual(Email.objects.last().to, [self.jeddah_media_center.coordinator.email])
