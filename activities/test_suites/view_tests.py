# -*- coding: utf-8  -*-
from django.contrib.auth.models import Permission, User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase
from accounts.test_utils import create_user
from activities.models import Activity, Review
from activities.test_utils import create_activity, add_presidency_review, add_deanship_review
from clubs.models import Club
from clubs.test_utils import add_club_member, set_club_coordinator
from clubs.utils import get_presidency, get_deanship


class ShowActivityViewTests(TestCase):
    fixtures = ['default_clubs.json']
    def setUp(self):
        self.submitter = create_user()
        self.user = create_user()
        self.activity1 = create_activity(submitter=self.submitter)
        self.activity2 = create_activity(submitter=self.submitter)

        self.client.login(username=self.user.username, password="12345678")

    def test_with_superuser(self):
        self.user.is_superuser = True
        self.user.save()
        self.util_no_restriction_users()

    def test_with_presidency(self):
        add_p_review = Permission.objects.get(codename="add_presidency_review")
        self.user.user_permissions.add(add_p_review)
        # sanity check
        self.assertTrue(self.user.has_perm('activities.add_presidency_review'))
        self.util_no_restriction_users()

    def test_with_primary_coodinator(self):
        club = self.activity1.primary_club
        club.coordinator = self.user
        club.save()
        self.util_no_restriction_users()

    def test_with_secondary_coordinator(self):
        pass

    def util_no_restriction_users(self):
        # Test with pending activity
        response = self.client.get(reverse('activities:show', args=(self.activity1.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.activity1.name)  # sanity check

        # Test with rejected activity
        add_presidency_review(self.activity1, False)
        response = self.client.get(reverse('activities:show', args=(self.activity1.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.activity1.name)  # sanity check

        # Test with approved activity
        add_presidency_review(self.activity2, True)
        add_deanship_review(self.activity2, True)
        response = self.client.get(reverse('activities:show', args=(self.activity2.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.activity2.name)  # sanity check

    def test_with_deanship_reviewer(self):
        add_d_review = Permission.objects.get(codename="add_deanship_review")
        self.user.user_permissions.add(add_d_review)

        # Test with pending activity
        response = self.client.get(reverse('activities:show', args=(self.activity1.pk, )))
        self.assertEqual(response.status_code, 403)

        # Test with activity approved by presidency
        add_presidency_review(self.activity1, True)
        response = self.client.get(reverse('activities:show', args=(self.activity1.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.activity1.name)  # sanity check

        # Test with rejected activity
        add_deanship_review(self.activity1, False)
        response = self.client.get(reverse('activities:show', args=(self.activity1.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.activity1.name)  # sanity check

        # Test with approved activity
        add_presidency_review(self.activity2, True)
        add_deanship_review(self.activity2, True)
        response = self.client.get(reverse('activities:show', args=(self.activity2.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.activity2.name)  # sanity check

    def test_with_normal_user(self):
        # Test with pending activity
        response = self.client.get(reverse('activities:show', args=(self.activity1.pk, )))
        self.assertEqual(response.status_code, 403)

        # Test with activity approved by presidency
        add_presidency_review(self.activity1, True)
        response = self.client.get(reverse('activities:show', args=(self.activity1.pk, )))
        self.assertEqual(response.status_code, 403)

        # Test with rejected activity
        add_deanship_review(self.activity1, False)
        response = self.client.get(reverse('activities:show', args=(self.activity1.pk, )))
        self.assertEqual(response.status_code, 403)

        # Test with approved activity
        add_presidency_review(self.activity2, True)
        add_deanship_review(self.activity2, True)
        response = self.client.get(reverse('activities:show', args=(self.activity2.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.activity2.name)  # sanity check

    def test_show_view_with_a_normal_user(self):
        """
        Test the show activity view with a user with no permissions.
        """
        # Setup the database
        normal_user = create_user('normal_user')
        club = create_club()
        activity = create_activity(submitter=normal_user, club=club)
        add_presidency_review(activity, True)
        add_deanship_review(activity, True)

        # Login
        logged_in = self.client.login(username=normal_user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        response = self.client.get(reverse('activities:show',
                                           args=(activity.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, activity.name)
        self.assertContains(response, activity.primary_club.name)
        # self.assertContains(response, activity.description)
        # Normal user should not see activity status
        self.assertNotContains(response, 'tooltip-primary')
        # Normal user should not see edit button
        self.assertNotContains(response, 'href="' + reverse('activities:edit',
                                                            args=(activity.pk, )) + '"'
                               )
        # Normal user should not see review buttons
        self.assertNotContains(response, u'مراجعة رئاسة نادي الطلاب')
        self.assertNotContains(response, u'مراجعة عمادة شؤون الطلاب')

    def test_show_view_with_a_privileged_user(self):
        privileged_user = create_user('user2')

        view_activity = Permission.objects.get(codename='view_activity')
        change_activity = Permission.objects.get(codename='change_activity')
        view_deanship_review = Permission.objects.get(codename='view_deanship_review')
        view_presidency_review = Permission.objects.get(codename='view_presidency_review')
        privileged_user.user_permissions.add(view_activity, change_activity,
                                             view_deanship_review, view_presidency_review)

        club = create_club()
        activity = create_activity(submitter=privileged_user)

        # Login
        logged_in = self.client.login(username=privileged_user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        response = self.client.get(reverse('activities:show',
                                           args=(activity.pk, )))

        # Housekeeping tests
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, activity.name)
        self.assertContains(response, activity.primary_club.name)
        self.assertContains(response, activity.description)

        # Privileged user should see activity status
        self.assertContains(response, 'tooltip-primary')
        # Privileged user should see edit button
        self.assertContains(response, 'href="' + reverse('activities:edit',
                                                        args=(activity.pk, )) + '"'
                            )
        # Privileged user should see review buttons
        self.assertContains(response, u'مراجعة رئاسة نادي الطلاب')
        self.assertContains(response, u'مراجعة عمادة شؤون الطلاب')


class ListActivityViewTests(TestCase):
    """
    Tests for behavior of list_activities view with different users and permissions.
    """
    # fixtures = ['initial_data.json']
    def setUp(self):
        self.presidency = create_club(english_name="Presidency")
        self.media_center = create_club(english_name="Media Center")
        self.club = create_club()
        self.club2 = create_club()
        self.user = create_user(username="msarabi")
        self.client.login(username=self.user.username, password="12345678")

        # The following activities represent the 7 common patterns for activities in terms of their approval status.
        # The naming of the following activities follows this pattern: activity_[P][D],
        # where [P] represents the status of the activity's presidency review
        # and [D] represents  the status of the activity's DSA review.
        # The possible statuses are n (nonexistent), p (pending), r (rejected), and a (approved).
        self.activity_nn = create_activity(club=self.club)  # no review
        self.activity_pn = add_presidency_review(create_activity(club=self.club2), None)  # and add reviews # p: pending, n: none
        self.activity_rn = add_presidency_review(create_activity(club=self.club2), False)
        self.activity_an = add_presidency_review(create_activity(club=self.club), True)
        self.activity_ap = add_deanship_review(add_presidency_review(create_activity(club=self.club), True), None)
        self.activity_ar = add_deanship_review(add_presidency_review(create_activity(club=self.club), True), False)
        self.activity_aa = add_deanship_review(add_presidency_review(create_activity(club=self.club), True), True)

    def tearDown(self):
        self.client.logout()

    def test_list_view_with_superuser(self):
        self.user.is_superuser = True
        self.user.save()
        self.assertTrue(User.objects.get(username="msarabi").is_superuser)  # sanity check
        self.util_superuser_and_presidency()

    def test_list_view_with_presidency_coordinator(self):
        set_club_coordinator(get_presidency(), self.user)
        self.util_superuser_and_presidency()

    def test_list_view_with_presidency_member(self):
        add_club_member(get_presidency(), self.user)
        self.util_superuser_and_presidency()

    def util_superuser_and_presidency(self):
        """
        A utility method to reduce repetition in the previous 3 tests.
        """
        response = self.client.get(reverse('activities:list'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(sorted(list(response.context['approved'])), sorted(list(Activity.objects.approved())))
        # self.assertEqual(sorted(list(response.context['pending'])), sorted(list(get_pending_activities())))
        # self.assertEqual(sorted(list(response.context['rejected'])), sorted(list(get_rejected_activities())))

        self.assertIn(self.activity_nn, response.context['pending'])
        self.assertIn(self.activity_pn, response.context['pending'])
        self.assertIn(self.activity_rn, response.context['rejected'])
        self.assertIn(self.activity_an, response.context['pending'])
        self.assertIn(self.activity_ap, response.context['pending'])
        self.assertIn(self.activity_ar, response.context['rejected'])
        self.assertIn(self.activity_aa, response.context['approved'])

    def test_list_view_with_dsa_reviewer(self):
        """
        Test that Deanship of Student Affairs reviewers only see activities approved by students club presidency.
        """
        # print Group.objects.all()
        # group = Group.objects.get(name='deanship_master')
        # group.user_set.add(self.user)
        can_add_deanship_review = Permission.objects.get(codename="add_deanship_review")
        self.user.user_permissions.add(can_add_deanship_review)
        self.user.save()
        self.assertTrue(self.user.has_perm('activities.add_deanship_review'))  # sanity check

        response = self.client.get(reverse('activities:list'))
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(self.activity_nn, response.context['pending'])
        self.assertNotIn(self.activity_pn, response.context['pending'])
        self.assertNotIn(self.activity_rn, response.context['rejected'])
        self.assertIn(self.activity_an, response.context['pending'])
        self.assertIn(self.activity_ap, response.context['pending'])
        self.assertIn(self.activity_ar, response.context['rejected'])
        self.assertIn(self.activity_aa, response.context['approved'])

    def test_list_view_with_club_coordinator(self):
        """
        Test that club coordinators can only see approved activities in addition to pending and rejected activities
        of their own club.
        """
        set_club_coordinator(self.club2, self.user)
        self.util_club_coordinator_and_member()

    def test_list_view_with_club_member(self):
        """
        Test that club members can only see approved activities in addition to pending and rejected activities
        of their own club.
        """
        add_club_member(self.club2, self.user)
        self.util_club_coordinator_and_member()

    def util_club_coordinator_and_member(self):
        """
        A utility function to reduce repetition in the previous 2 tests.
        """
        response = self.client.get(reverse('activities:list'))
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(self.activity_nn, response.context['pending'])
        self.assertIn(self.activity_pn, response.context['pending'])
        self.assertIn(self.activity_rn, response.context['rejected'])
        self.assertNotIn(self.activity_an, response.context['pending'])
        self.assertNotIn(self.activity_ap, response.context['pending'])
        self.assertNotIn(self.activity_ar, response.context['rejected'])
        self.assertIn(self.activity_aa, response.context['approved'])

    def test_list_view_with_employee(self):
        """
        Test that an employee will have two tables: (1) all approved activities (including their clubs')
        (2) their clubs' approved activities
        """
        self.employee = create_user()
        self.club2.employee = self.employee
        self.club2.save()

        self.another_approved_activity = add_deanship_review(add_presidency_review(create_activity(club=self.club2),
                                                                                   True), True)
        self.client.login(username=self.employee.username, password="12345678")
        response = self.client.get(reverse('activities:list'))
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(self.activity_nn, response.context['pending'])
        self.assertNotIn(self.activity_pn, response.context['pending'])
        self.assertNotIn(self.activity_rn, response.context['rejected'])
        self.assertNotIn(self.activity_an, response.context['pending'])
        self.assertNotIn(self.activity_ap, response.context['pending'])
        self.assertNotIn(self.activity_ar, response.context['rejected'])
        self.assertIn(self.activity_aa, response.context['approved'])
        self.assertIn(self.another_approved_activity, response.context['approved'])

        self.assertNotIn(self.activity_aa, response.context['club_approved'])
        self.assertIn(self.another_approved_activity, response.context['club_approved'])


    def test_list_view_with_normal_user(self):
        """
        Test that a normal user will only see approved activities.
        """
        # Don't do anything with the user

        response = self.client.get(reverse('activities:list'))
        self.assertEqual(response.status_code, 200)

        self.assertNotIn(self.activity_nn, response.context['pending'])
        self.assertNotIn(self.activity_pn, response.context['pending'])
        self.assertNotIn(self.activity_rn, response.context['rejected'])
        self.assertNotIn(self.activity_an, response.context['pending'])
        self.assertNotIn(self.activity_ap, response.context['pending'])
        self.assertNotIn(self.activity_ar, response.context['rejected'])
        self.assertIn(self.activity_aa, response.context['approved'])

def create_club(name="Test Club Arabic Name",
                english_name="Test English Club Name"):
    return Club.objects.create(name=name,
                               english_name=english_name,
                               description="-",
                               email="test@enjazportal.com",
                               )