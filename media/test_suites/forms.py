from django.test import TestCase
from accounts.test_utils import create_user
from clubs.utils import get_media_center
from media.forms import TaskForm


class TaskFormTests(TestCase):
    def setUp(self):
        self.user1 = create_user()
        self.user2 = create_user()

    def test_init(self):
        """
        Test the queryset restriction specified on the assignee field.
        """
        self.user1.memberships.add(get_media_center())
        self.assertIn(self.user1, get_media_center().members.all())

        self.form = TaskForm()
        self.assertIn(self.user1, self.form.assignee.queryset)
        self.assertNotIn(self.user2, self.form.assignee.queryset)