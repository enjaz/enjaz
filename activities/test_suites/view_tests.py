# coding=utf-8
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.test import TestCase
from accounts.test_utils import create_user
from activities.models import Review
from activities.test_utils import create_activity
from clubs.models import Club


class ShowActivityViewTests(TestCase):
    def test_show_view_with_a_normal_user(self):
        """
        Test the show activity view with a user with no permissions.
        """
        # Setup the database
        normal_user = create_user('normal_user')
        club = create_club()
        activity = create_activity(submitter=normal_user, club=club)
        
        # Login
        logged_in = self.client.login(username=normal_user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        response = self.client.get(reverse('activities:show',
                                           args=(activity.pk, )))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, activity.name)
        self.assertContains(response, activity.primary_club.name)
        self.assertContains(response, activity.description)
        # Normal user should not see activity status
        self.assertNotContains(response, 'tooltip-primary')
        # Normal user should not see edit button
        self.assertNotContains(response, 'href="' + reverse('activities:edit',
                                                            args=(activity.pk, )) + '"'
                               )
        # Normal user should not see review buttons
        self.assertNotContains(response, u'مراجعة رئاسة نادي الطلاب')
        self.assertNotContains(response, u'مراجعة عمادة شؤون الطلاب')

    def test_show_view_with_a_normal_user_and_collect_participants(self):
        """
        Test whether the user can see participate button.
        """
        # Setup the database
        normal_user = create_user('normal_user')
        club = create_club()
        activity = create_activity(submitter=normal_user,
                                   collect_participants=True)

        # Login
        logged_in = self.client.login(username=normal_user.username, password='12345678')
        self.assertEqual(logged_in, True)

        response = self.client.get(reverse('activities:show',
                                   args=(activity.pk, )))
        self.assertContains(response, 'href="' + reverse('activities:participate',
                                                         args=(activity.pk, )) + '"'
                            )

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


class ReviewViewTests(TestCase):
    def test_review_view_with_normal_user(self):
        # Setup the database
        normal_user = create_user('normal_user')
        club = create_club()
        activity = create_activity(submitter=normal_user)

        # Login
        logged_in = self.client.login(username=normal_user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        response = self.client.get(reverse('activities:review',
                                           args=(activity.pk, )))
        self.assertEqual(response.status_code, 403) # Forbidden

        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'p')))
        self.assertEqual(response.status_code, 403) # Forbidden

        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'd')))
        self.assertEqual(response.status_code, 403) # Forbidden

    def test_review_view_with_view_presidency_permission_and_no_review(self):
        """
        Test how the review view appears with a user who has a view presidency
        permission and when the activity hasn't been reviewed by presidency yet.
        """
        # Setup the database
        user = create_user('user')
        club = create_club()
        activity = create_activity(submitter=user, club=club)

        view_presidency_review = Permission.objects.get(codename='view_presidency_review')
        user.user_permissions.add(view_presidency_review)

        # Login
        logged_in = self.client.login(username=user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        # The follow argument keeps track of the redirects
        # https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.Client.get
        response = self.client.get(reverse('activities:review',
                                           args=(activity.pk, )),
                                   follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302) # make sure we're redirected
        # make sure we're redirected to /review/p/
        self.assertEqual(response.request['PATH_INFO'], reverse('activities:review_with_type',
                                                                args=(activity.pk, 'p')))
        self.assertEqual(response.status_code, 200)

        # some more housekeeping tests
        self.assertContains(response, activity.name)
        self.assertContains(response, activity.primary_club.name)
        self.assertContains(response, activity.description)

        # user should see presidency but not deanship review buttons
        self.assertContains(response, u'مراجعة رئاسة نادي الطلاب')
        self.assertNotContains(response, u'مراجعة عمادة شؤون الطلاب')

        # Should see error message
        self.assertContains(response, '<i class="entypo-hourglass"></i>') # hourglass
        self.assertContains(response, '<p>هذا النشاط لم تتم مراجعته بعد.</p>') # message

        # Try visiting deanship review page
        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'd')))
        self.assertEqual(response.status_code, 403) # Forbidden

    def test_review_view_with_view_presidency_permission_and_review(self):
        """
        Test how the review view appears with a user who has a view presidency
        permission and when the activity has been reviewed by presidency.
        """
        # Setup the database
        user = create_user('user')
        club = create_club()
        activity = create_activity(submitter=user, club=club)
        review = Review.objects.create(activity=activity,
                                       name_notes="Test Name Notes",
                                       review_type="P")

        view_presidency_review = Permission.objects.get(codename='view_presidency_review')
        user.user_permissions.add(view_presidency_review)

        # Login
        logged_in = self.client.login(username=user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        # The follow argument keeps track of the redirects
        # https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.Client.get
        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'p')))
        self.assertEqual(response.status_code, 200)

        # some more housekeeping tests
        self.assertContains(response, activity.name)
        self.assertContains(response, activity.primary_club.name)
        self.assertContains(response, activity.description)

        # user should see presidency but not deanship review buttons
        self.assertContains(response, u'مراجعة رئاسة نادي الطلاب')
        self.assertNotContains(response, u'مراجعة عمادة شؤون الطلاب')

        # Should see review
        self.assertContains(response, 'panel-body with-table') # panel
        self.assertContains(response, review.name_notes)
        self.assertContains(response, '<div class="label label-warning">معلَّق</div>')

        # should not see submit button
        self.assertNotContains(response, '<button type="submit"')
        self.assertNotContains(response, 'أرسل')

    def test_review_view_with_view_deanship_permission_and_no_review(self):
        """
        Test how the review view appears with a user who has a view deanship
        permission and when the activity hasn't been reviewed by deanship yet.
        """
        # Setup the database
        user = create_user('user')
        club = create_club()
        activity = create_activity(submitter=user, club=club)

        view_deanship_review = Permission.objects.get(codename='view_deanship_review')
        user.user_permissions.add(view_deanship_review)

        # Login
        logged_in = self.client.login(username=user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        # The follow argument keeps track of the redirects
        # https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.Client.get
        response = self.client.get(reverse('activities:review',
                                           args=(activity.pk, )),
                                   follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302) # make sure we're redirected
        # make sure we're redirected to /review/p/
        self.assertEqual(response.request['PATH_INFO'], reverse('activities:review_with_type',
                                                                args=(activity.pk, 'd')))
        self.assertEqual(response.status_code, 200)

        # some more housekeeping tests
        self.assertContains(response, activity.name)
        self.assertContains(response, activity.primary_club.name)
        self.assertContains(response, activity.description)

        # user should see deanship but not presidency review buttons
        self.assertNotContains(response, u'مراجعة رئاسة نادي الطلاب')
        self.assertContains(response, u'مراجعة عمادة شؤون الطلاب')

        # Should see error message
        self.assertContains(response, '<i class="entypo-hourglass"></i>') # hourglass
        self.assertContains(response, '<p>هذا النشاط لم تتم مراجعته بعد.</p>') # message

        # Try visiting deanship review page
        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'p')))
        self.assertEqual(response.status_code, 403) # Forbidden

    def test_review_view_with_view_deanship_permission_and_review(self):
        """
        Test how the review view appears with a user who has a view deanship
        permission and when the activity has been reviewed by deanship.
        """
         # Setup the database
        user = create_user('user')
        club = create_club()
        activity = create_activity(submitter=user, club=club)
        review = Review.objects.create(activity=activity,
                                       name_notes="Test Name Notes",
                                       review_type="D")

        view_deanship_review = Permission.objects.get(codename='view_deanship_review')
        user.user_permissions.add(view_deanship_review)

        # Login
        logged_in = self.client.login(username=user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        # The follow argument keeps track of the redirects
        # https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.Client.get
        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'd')))
        self.assertEqual(response.status_code, 200)

        # some more housekeeping tests
        self.assertContains(response, activity.name)
        self.assertContains(response, activity.primary_club.name)
        self.assertContains(response, activity.description)

        # user should see deanship but not presidency review buttons
        self.assertNotContains(response, u'مراجعة رئاسة نادي الطلاب')
        self.assertContains(response, u'مراجعة عمادة شؤون الطلاب')

        # Should see review
        self.assertContains(response, "panel-body with-table") # panel
        self.assertContains(response, review.name_notes)
        self.assertContains(response, '<div class="label label-warning">معلَّق</div>')

        # should not see submit button
        self.assertNotContains(response, '<button type="submit"')
        self.assertNotContains(response, 'أرسل')

    def test_review_view_with_add_presidency_permission_and_no_review(self):
        """
        Test how the review view appears with a user who has an add presidency
        permission and when the activity hasn't yet been reviewed by presidency.
        """
        # Setup the database
        user = create_user('user')
        club = create_club()
        activity = create_activity(submitter=user, club=club)

        add_presidency_review = Permission.objects.get(codename='add_presidency_review')
        user.user_permissions.add(add_presidency_review)

        # Login
        logged_in = self.client.login(username=user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        # The follow argument keeps track of the redirects
        # https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.Client.get
        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'p')))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "panel-body with-table") # panel

        # Should not see status label (only in read mode)
        self.assertNotContains(response, '<div class="label label-warning">معلَّق</div>')

        # should see form and submit button
        self.assertContains(response, '<form action="' + reverse('activities:review_with_type',
                                                                 args=(activity.pk, 'p')))
        self.assertContains(response, '<button type="submit"')
        self.assertContains(response, 'أرسل')

    def test_review_view_with_add_presidency_permission_and_review(self):
        """
        Test how the review view appears with a user who has an add presidency
        permission and when the activity has been reviewed by presidency.
        """
        # Setup the database
        user = create_user('user')
        club = create_club()
        activity = create_activity(submitter=user, club=club)
        review = Review.objects.create(activity=activity,
                                       name_notes="Test Name Notes",
                                       review_type="P")

        add_presidency_review = Permission.objects.get(codename='add_presidency_review')
        user.user_permissions.add(add_presidency_review)

        # Login
        logged_in = self.client.login(username=user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        # The follow argument keeps track of the redirects
        # https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.Client.get
        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'p')))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "panel-body with-table") # panel

        # Should not see status label (only in read mode)
        self.assertNotContains(response, '<div class="label label-warning">معلَّق</div>')

        # should see form and submit button
        self.assertContains(response, '<form action="' + reverse('activities:review_with_type',
                                                                 args=(activity.pk, 'p')))
        self.assertContains(response, '<button type="submit"')
        self.assertContains(response, 'أرسل')
        self.assertContains(response, review.name_notes)

    def test_review_view_with_add_deanship_permission_and_no_review(self):
        """
        Test how the review view appears with a user who has an add deanship
        permission and when the activity hasn't yet been reviewed by deanship.
        """
        # Setup the database
        user = create_user('user')
        club = create_club()
        activity = create_activity(submitter=user, club=club)

        add_deanship_review = Permission.objects.get(codename='add_deanship_review')
        user.user_permissions.add(add_deanship_review)

        # Login
        logged_in = self.client.login(username=user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        # The follow argument keeps track of the redirects
        # https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.Client.get
        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'd')))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "panel-body with-table") # panel

        # Should not see status label (only in read mode)
        self.assertNotContains(response, '<div class="label label-warning">معلَّق</div>')

        # should see form and submit button
        self.assertContains(response, '<form action="' + reverse('activities:review_with_type',
                                                                 args=(activity.pk, 'd')))
        self.assertContains(response, '<button type="submit"')
        self.assertContains(response, 'أرسل')

    def test_review_view_with_add_deanship_permission_and_review(self):
        """
        Test how the review view appears with a user who has an add deanship
        permission and when the activity has been reviewed by deanship.
        """
        # Setup the database
        user = create_user('user')
        club = create_club()
        activity = create_activity(submitter=user, club=club)
        review = Review.objects.create(activity=activity,
                                       name_notes="Test Name Notes",
                                       review_type="D")

        add_deanship_review = Permission.objects.get(codename='add_deanship_review')
        user.user_permissions.add(add_deanship_review)

        # Login
        logged_in = self.client.login(username=user.username, password='12345678')
        self.assertEqual(logged_in, True)

        # Go to the view
        # The follow argument keeps track of the redirects
        # https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.Client.get
        response = self.client.get(reverse('activities:review_with_type',
                                           args=(activity.pk, 'd')))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "panel-body with-table") # panel

        # Should not see status label (only in read mode)
        self.assertNotContains(response, '<div class="label label-warning">معلَّق</div>')

        # should see form and submit button
        self.assertContains(response, '<form action="' + reverse('activities:review_with_type',
                                                                 args=(activity.pk, 'd')))
        self.assertContains(response, '<button type="submit"')
        self.assertContains(response, 'أرسل')
        self.assertContains(response, review.name_notes)


def create_club():
    return Club.objects.create(name="Test Club Arabic Name",
                               english_name="Test English Club Name",
                               description="-",
                               email="test@enjazportal.com",
                               )