# coding=utf-8
from django.contrib.auth.models import User
from django.test import TestCase

from events.models import Survey


class AdminTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='abcd1234',
        )
        self.user1.is_staff = True
        self.user1.save()

        self.client.login(
            username='testuser1',
            password='abcd1234',
        )

        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='abcd1234',
        )

        self.user3 = User.objects.create_user(
            username='testuser3',
            email='test3@example.com',
            password='abcd1234',
        )

    def test_download_survey_results_as_excel(self):
        survey = Survey.objects.create(name="Feedback")
        question1 = survey.survey_questions.create(
            category='O',
            text=u"ما هي هوايتك المفضلة؟",
        )
        question2 = survey.survey_questions.create(
            category='C',
            choices=u"لندن\nباريس",
            text=u"إلى أين تود الذهاب في الإجازة القادمة؟",
        )

        response1 = survey.responses.create(
            user=self.user2,
        )
        response1.answers.create(
            question=question1,
            text_value=u"الرسم",
        )
        response1.answers.create(
            question=question2,
            text_value=u"لندن",
        )

        response2 = survey.responses.create(
            user=self.user3,
        )
        response2.answers.create(
            question=question1,
            text_value=u"السباحة",
        )
        response2.answers.create(
            question=question2,
            text_value=u"باريس",
        )

        response = self.client.get("/admin/events/survey/{}/results/".format(survey.id))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.get('Content-Disposition'),
            "attachment; filename={}".format("Survey Results.xlsx")
        )

        self.assertEqual(
            response.get('Content-Type'),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8"
        )
