from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email
from django.db import IntegrityError
from accounts.models import CommonProfile
from events.models import Event
from post_office import mail
import random
import string
import unicodecsv


class Command(BaseCommand):
    help = "Creat new accounts"

    def add_arguments(self, parser):
        parser.add_argument('--csv-file')
        parser.add_argument('--profile-type')
        parser.add_argument('--event-code-name', default=None)
        parser.add_argument('--email-template')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        profile_type = options['profile_type']
        email_template = options['email_template']
        event_code_name = options['event_code_name']
        if event_code_name:
            event = Event.objects.get(code_name=event_code_name)
            sender_email = event.get_notification_email()
        else:
            event = None
            sender_email = None
        csv_reader = unicodecsv.reader(open(csv_file), encoding="utf-8")

        for row in csv_reader:
            email = row[0].strip()
            try:
                validate_email(email)
            except ValidationError:
                print email, "is not a valid email address"
                continue
            tokens = email.split('@')
            username = tokens[0]
            random_password = "".join([random.choice(string.digits + string.uppercase) for i in range(8)])
            user = (User.objects.filter(email=email) | User.objects.filter(username=username)).first()
            if user:
                preexisting = True
                user.set_password(random_password)
                print email, "already has an account!  Sending a new password..."
            else:
                preexisting = False
                user = User.objects.create_user(username, email, random_password)
                ar_first_name = row[1]
                ar_middle_name = row[2]
                ar_last_name = row[3]
                en_first_name = row[4]
                en_middle_name = row[5]
                en_last_name = row[6]
                alternative_email = row[7]
                badge_number = row[8] or None
                mobile_number = row[9]
                city = row[10]
                gender = row[11]
                CommonProfile.objects.create(user=user,
                                             profile_type=profile_type,
                                             ar_first_name=ar_first_name,
                                             ar_middle_name=ar_middle_name,
                                             ar_last_name=ar_last_name,
                                             en_first_name=en_first_name,
                                             en_middle_name=en_middle_name,
                                             en_last_name=en_last_name,
                                             alternative_email=alternative_email,
                                             badge_number=badge_number,
                                             city=city,
                                             gender=gender)
                print "Created an account for", email
            if event:
                event.abstract_revision_team.members.add(user)
            mail.send([user.email], template=email_template,
                      context={'user': user, 'random_password': random_password,
                               'preexisting': preexisting, 'event': event})
