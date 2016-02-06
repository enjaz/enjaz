from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from userena.models import UserenaSignup


class Command(BaseCommand):
    help = "Notify users to update."

    def handle(self, *args, **options):
        for user in User.objects.filter(is_active=False, userena_signup__isnull=False):
            new_key = UserenaSignup.objects.reissue_activation(user.userena_signup.activation_key)
            self.stdout.write(u'Email with {}'.format(user.email))
