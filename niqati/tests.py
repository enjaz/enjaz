# -*- coding: utf-8  -*-
import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
from accounts.test_utils import create_user
from activities.models import Evaluation
from activities.test_utils import create_activity

from .models import Category, Code, Code_Collection, Code_Order


def create_code(activity, category, collection):
    code = Code.objects.create(activity=activity,
                               category=category,
                               collection=collection)
    code.generate_unique()
    code.save()
    return code


def create_codes(count, activity=create_activity(),
                 category=Category.objects.get(pk=1)):

    order = Code_Order.objects.create(activity=activity)
    collec = Code_Collection.objects.create(parent_order=order,
                                            code_category=category,
                                            code_count=count,
                                            delivery_type='0',
    )
    for i in range(count):
        create_code(activity=activity,
                    category=category,
                    collection=collec,
        )


class SubmitCodeTests(TestCase):
    """
    Tests for code submission and activity evaluation.
    """
    fixtures = ['initial_data.json']

    def setUp(self):
        self.user = create_user()
        self.activity = create_activity()
        create_codes(5, activity=self.activity, category=Category.objects.get(points=1))
        create_codes(5, activity=self.activity, category=Category.objects.get(points=2))
        create_codes(5, activity=self.activity, category=Category.objects.get(points=3))
        self.client.login(username=self.user.username, password='12345678')

    def tearDown(self):
        self.client.logout()

    def test_submit_code_no_issues(self):
        """
        Test a 'Sunny day scenario:'
        A user has no other codes in the same activity.
        """
        self.code = Code.objects.get(pk=1)

        # before submission, the user should not have any evaluations for the activity
        self.assertQuerysetEqual(Evaluation.objects.filter(evaluator=self.user, activity=self.activity),
                                 Evaluation.objects.none())

        response = self.client.post(reverse("niqati:submit"),
                                    {'code': self.code.code_string,
                                     'relevance': '4',
                                     'quality': '3'}
                                    )

        self.assertEqual(response.status_code, 200)
        # niqati tests
        self.assertIn(self.code, self.user.code_set.all())
        #self.assertEqual(self.code.user, self.user)
        #self.assertEqual(self.code.redeem_date, datetime.datetime.now())
        self.assertContains(response, u"تم تسجيل الرمز بنجاح.")

        # evaluation tests
        self.assertEqual(Evaluation.objects.filter(evaluator=self.user, activity=self.activity).count(), 1)
        self.evaluation = Evaluation.objects.get(evaluator=self.user, activity=self.activity)
        self.assertEqual(self.evaluation.relevance, 4)
        self.assertEqual(self.evaluation.quality, 3)


    def test_submit_code_with_other_code_of_less_value(self):
        """
        Test a scenario where a user already has a code in the same activity, but whose value is
        less than the submitted code. In this case it should be replaced.
        """
        self.code_cheap = Code.objects.filter(category__points=1).first()
        self.code = Code.objects.filter(category__points=2).first()

        # Add the cheap code to the user first
        self.code_cheap.user = self.user
        self.code_cheap.save()

        # Since the user already has a previous code, they must also have submitted an evaluation
        self.evaluation = Evaluation.objects.create(activity=self.activity,
                                                    evaluator=self.user,
                                                    relevance=2,
                                                    quality=4)

        # Now submit the new code
        response = self.client.post(reverse("niqati:submit"),
                                    {'code': self.code.code_string,
                                     'relevance': 5,
                                     'quality': 1}
                                    )

        # niqati tests
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.code_cheap, self.user.code_set.all())
        self.assertIn(self.code, self.user.code_set.all())
        self.assertContains(response, u"تم إدخال الرمز بنجاح و استبدال الرمز السابق لك في هذا النشاط.")

        # evaluation tests
        # no new evaluations should be added; the existing evaluation should be updated only
        self.assertEqual(Evaluation.objects.filter(activity=self.activity, evaluator=self.user).count(), 1)
        self.assertEqual(Evaluation.objects.get(activity=self.activity, evaluator=self.user), self.evaluation)
        self.evaluation = Evaluation.objects.get(activity=self.activity, evaluator=self.user)
        self.assertEqual(self.evaluation.relevance, 5)
        self.assertEqual(self.evaluation.quality, 1)

    def utility_greater_or_equal(self):
        """
        A utility function that combines the two tests below.
        """
        # Add the valuable code to the user first
        self.code_valuable.user = self.user
        self.code_valuable.save()

        self.code = Code.objects.filter(category__points=2)\
            .exclude(user=self.user).first()  # Make sure to exclude the other code
                                              # (in case of equality)

        # Now submit the new code
        response = self.client.post(reverse("niqati:submit"),
                                    {'code': self.code.code_string}
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.code_valuable, self.user.code_set.all())
        self.assertNotIn(self.code, self.user.code_set.all())
        self.assertContains(response,
                            u"لا يمكن إدخال هذا الرمز؛ لديك رمز نقاطي آخر في نفس النشاط ذو قيمة مساوية أو أكبر.")

    def test_submit_code_with_other_code_of_greater_value(self):
        """
        Test a scenario where a user already has a code in the same activity, and whose value is greater
        than the one submitted. In this case it should be rejected.
        """
        # a code with greater value
        self.code_valuable = Code.objects.filter(category__points=3).first()
        self.utility_greater_or_equal()

    def test_submit_code_with_other_code_of_equal_value(self):
        """
        Test a scenario where a user already has a code in the same activity, and whose value is equal
        to the one submitted. In this case it should be rejected.
        """
        # a code with greater value
        self.code_valuable = Code.objects.filter(category__points=2).first()
        self.utility_greater_or_equal()

    def test_submit_code_twice(self):
        """
        Test submitting a code twice. Should be rejected of course.
        """
        self.code = Code.objects.get(pk=1)

        # Assign the code to the user
        self.code.user = self.user
        self.code.save()

        # Submit it again
        response = self.client.post(reverse("niqati:submit"),
                                    {'code': self.code.code_string}
                                    )

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.code, self.user.code_set.all())
        self.assertContains(response, u"لقد استخدمت هذا الرمز من قبل؛ لا يمكنك استخدامه مرة أخرى")

    def test_submit_code_used_by_other_user(self):
        """
        Test submitting a code used by another user. Rejection expected.
        """
        self.code = Code.objects.get(pk=1)

        # Assign the code to another user
        self.code.user = create_user()  # a random user
        self.code.save()

        # Submit it
        response = self.client.post(reverse("niqati:submit"),
                                    {'code': self.code.code_string}
                                    )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.code, self.user.code_set.all())
        self.assertContains(response, u"هذا الرمز غير متوفر.")

    def test_submit_invalid_code(self):
        """
        Test submitting an invalid code, or a code that doesn't exist.
        """
        response = self.client.post(reverse("niqati:submit"),
                                    {'code': '12345'}  # An invalid code
                                    )

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(self.user.code_set.all(), Code.objects.none())
        self.assertContains(response, u"هذا الرمز غير صحيح.")