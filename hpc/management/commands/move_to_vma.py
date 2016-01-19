import os
import urllib2
import unicodecsv

from django.core.management.base import BaseCommand

from hpc.models import Session


class Command(BaseCommand):
    help = "Delete repeated non-user repetitions."

    def add_arguments(self, parser):
        parser.add_argument('directory')

    def register_in_vma(self, session, registration):
        en_full_name = registration.get_en_full_name()
        phone = registration.get_phone()
        email = registration.get_email()

        self.stdout.write(u"Posting {} to {}".format(email, session.name))

        if session.vma_time_code:
            response = urllib2.openurl("http://www.medicalacademy.org/portal/register/member/workshop/organizer?workshop_id={}&workshop_time_code={}&organizer=1&full_name={}&email={}&mobile={}".format(session.vma_id, session.vma_time_code, en_full_name, email, phone)).read()
        else:
            response = urllib2.openurl("http://www.medicalacademy.org/portal/register/member/event/organizer?event_id={}&organizer=1&full_name={}&email={}&mobile={}".format(session.vma_id, en_full_name, email, phone)).read()

        if response == 'true':
            registration.was_moved_to_vma = True
            registration.save()
        else:
            print "response was", response

    def handle(self, *args, **options):
        csv_files = os.listdir(options['directory'])
        self.stdout.write("Included files are: {}".format(", ".join(csv_files)))
        for session in Session.objects.all():
            csv_filename = str(session.pk) + '.csv'
            full_path = os.path.join(options['directory'], csv_filename)
            if os.path.isfile(full_path):
                self.stdout.write("{} exists".format(full_path))
                csv_file = open(full_path)
                csv_reader = unicodecsv(csv_file, encoding="utf-8")
                for row in csv_reader:
                    email = row[4]
                    registration = (Registration.objects.filter(nonuser__email=email) | \
                                    Registration.objects.filter(user__email=email)).first()
                    if registration.was_moved_to_vma:
                        self.stdout.write("{} was already moved".format(email))
                    elif registration.is_deleted:
                        self.stdout.write("{} was deleted".format(email))
                    self.register_in_vma(session, registration)

            else:
                self.stdout.write("{} is missing".format(full_path))
                while True:
                    answer = raw_input(u"Do you want to accept everybody for {}? (Y) ".format(session.name))
                    if answer.lower() == 'y':
                        break
                for registration in session.registration_set.filter(is_deleted=False, was_moved_to_vma=False):
                    self.register_in_vma(session, registration)

