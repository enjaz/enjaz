from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from model_mommy import mommy

from media.rules import is_media_center_coordinator, is_media_center_deputy, is_media_center_member, \
    is_media_representative_of_any_club


class TestMediaCenterPredicates(TestCase):
    def setUp(self):
        self.current_year = mommy.make(
            'core.StudentClubYear',
            start_date=timezone.make_aware(datetime(2017, 1, 1)),
            end_date=timezone.make_aware(datetime(2017, 12, 31)),
        )
        self.current_media_center = mommy.make('clubs.Club', english_name="Media Center", year=self.current_year)

        self.previous_year = mommy.make(
            'core.StudentClubYear',
            start_date=timezone.make_aware(datetime(2016, 1, 1)),
            end_date=timezone.make_aware(datetime(2016, 12, 31)),
        )
        self.previous_media_center = mommy.make('clubs.Club', english_name="Media Center", year=self.previous_year)

    # `is_media_center_coordinator` tests
    def test_includes_media_center_coordinator_of_current_year(self):
        """
        Any user who is coordinating a media center (regardless of city) during current year should pass.
        """
        self.user = mommy.make('auth.User')
        self.current_media_center.coordinator = self.user
        self.current_media_center.save()

        self.assertTrue(is_media_center_coordinator(self.user))

    def test_excludes_non_media_center_coordinator(self):
        """
        User who doesn't coordinate a media center should not pass.
        """
        self.user = mommy.make('auth.User')

        self.assertFalse(is_media_center_coordinator(self.user))

    def test_excludes_media_center_coordinator_of_different_year(self):
        """
        User coordinating a media center belonging to a year other than the current year should not pass.
        """
        self.user = mommy.make('auth.User')
        self.previous_media_center.coordinator = self.user
        self.previous_media_center.save()

        self.assertFalse(is_media_center_coordinator(self.user))

    # `is_media_center_deputy` tests
    def test_includes_media_center_deputy_of_current_year(self):
        """
        Any user who is a deputy of a media center (regardless of city) during current year should pass.
        """
        self.user = mommy.make('auth.User')
        self.current_media_center.deputies.add(self.user)

        self.assertTrue(is_media_center_deputy(self.user))

    def test_excludes_non_media_center_deputy(self):
        """
        User who isn't a deputy of a media center should not pass.
        """
        self.user = mommy.make('auth.User')

        self.assertFalse(is_media_center_deputy(self.user))

    def test_excludes_media_center_deputy_of_different_year(self):
        """
        A user who is a deputy of a media center belonging to a year other than the current year should not pass.
        """
        self.user = mommy.make('auth.User')
        self.previous_media_center.deputies.add(self.user)
        self.previous_media_center.save()

        self.assertFalse(is_media_center_deputy(self.user))

    # `is_media_center_member` tests
    def test_includes_media_center_member_of_current_year(self):
        """
        Any user who is a member of a media center (regardless of city) during current year should pass.
        """
        self.user = mommy.make('auth.User')
        self.current_media_center.members.add(self.user)

        self.assertTrue(is_media_center_member(self.user))

    def test_excludes_non_media_center_member(self):
        """
        User who isn't a member of a media center should not pass.
        """
        self.user = mommy.make('auth.User')

        self.assertFalse(is_media_center_member(self.user))

    def test_excludes_media_center_member_of_different_year(self):
        """
        A user who is a member of a media center belonging to a year other than the current year should not pass.
        """
        self.user = mommy.make('auth.User')
        self.previous_media_center.members.add(self.user)
        self.previous_media_center.save()

        self.assertFalse(is_media_center_member(self.user))


class TestMediaRepresentativePredicate(TestCase):
    def setUp(self):
        self.current_year = mommy.make(
            'core.StudentClubYear',
            start_date=timezone.make_aware(datetime(2017, 1, 1)),
            end_date=timezone.make_aware(datetime(2017, 12, 31)),
        )
        self.current_club = mommy.make('clubs.Club', year=self.current_year)

        self.previous_year = mommy.make(
            'core.StudentClubYear',
            start_date=timezone.make_aware(datetime(2016, 1, 1)),
            end_date=timezone.make_aware(datetime(2016, 12, 31)),
        )
        self.previous_club = mommy.make('clubs.Club', year=self.previous_year)

    def test_includes_media_representative_during_current_year(self):
        """
        Any user who is a media representative of a club (regardless of city) during current year should pass.
        """
        self.user = mommy.make('auth.User')
        self.current_club.media_representatives.add(self.user)
        self.current_club.save()

        self.assertTrue(is_media_representative_of_any_club(self.user))

    def test_excludes_non_media_representative(self):
        """
        User who isn't a media representative should not pass.
        """
        self.user = mommy.make('auth.User')

        self.assertFalse(is_media_representative_of_any_club(self.user))

    def test_excludes_media_representative_during_different_year(self):
        """
        A user who is a representative of a club belonging to a year other than the current year should not pass.
        """
        self.user = mommy.make('auth.User')
        self.previous_club.media_representatives.add(self.user)
        self.previous_club.save()

        self.assertFalse(is_media_representative_of_any_club(self.user))
