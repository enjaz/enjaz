from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import translation

from certificates.models import Certificate
from events.models import Attendance, Session, SessionRegistration
from post_office import mail

# Attendance rules:
#
# 1) The event certificate will require 5 sign-ins which can include
#    the general program, college programs and only the workshops of
#    the general program.
#
# 2) The college program certificates will require both sign-in and
#    sign-out.
#
# 3) The workshops will require either a sign-in or a sign-out.

# April 23, 24
days = [23, 24]

# Session pks
colleges =  range(118, 123)
workshops = range(85, 118)
GENERAL_PROGRAM_PK = 21

# Attendance categories
all_categories = ["I", "M", "O", ""]
no_mid_categories = ["I", "O", ""]

sessions = {}
for pk in workshops + colleges + [GENERAL_PROGRAM_PK]:
    sessions[pk] = Session.objects.get(pk=pk)

def generate_session_sertificate(user, session_pk):
    session = sessions[session_pk]
    name = accounts.utils.get_user_en_full_name(user)
    if not name:
        name = user.username

    if Certificate.objects.filter(sessions__pk=session_pk, user=user).exists():
        print "Skipping {} for {} as previously generated.".format(session.name, name)
        return
    texts = [name, session.title]
    session.certificate_template.generate_certificate(hpc_user, texts, content_object=session)

class Command(BaseCommand):
    help = "Generate HPC 2017 Certificates."

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        from_email = event.get_notification_email()
                                    .exclude(pk__in=generated_pks)
        domain = Site.objects.get_current().domain
        url = "https://{}{}".format(domain,
                                    reverse('certificates:list_certificates_per_user'))

        for hpc_user in User.objects.filter(session_registrations__attendance__isnull=False,
                                            session_registrations__session__event__code_name="hpc2-j").distinct():
            user_total = 0

            # Look into the General Progrram.  Check both April 23rd
            # and April 24th.
            for day in days:
                for category in all_categories:
                    if Attendance.objects.filter(session_registration__session__pk=GENERAL_PROGRAM_PK,
                                                 session_registration__user=hpc_user,
                                                 date_submitted__day=day,
                                                 category=category).exists():
                        user_total += 1

            # Check college programs
            for pk in colleges:
                count = 0
                for category in no_mid_categories:
                    if Attendance.objects.filter(session_registration__session__pk=pk,
                                                 session_registration__user=hpc_user,
                                                 category=category).exists():
                        count += 1
                if count == 1:
                    user_total += 1
                elif count >= 2:
                    user_total += 2
                    generate_session_certificate(hpc_user, pk)

            # Check workshop programs
            for pk in workshops:
                for category in no_mid_categories:
                    if Attendance.objects.filter(session_registration__session__pk=pk,
                                                 session_registration__user=hpc_user,
                                                 category=category).exists():
                        # Only the workshops of the second day (pk=44-49)
                        # interferred with the conference attendance.
                        if pk in range(44, 50):
                            user_total += 1
                        generate_session_certificate(hpc_user, pk)
                        break

            if user_total >= 5:
                texts = [hpc_user.common_profile.get_en_full_name()]
                session.event_certificate_template.generate_certificate(hpc_user, texts, content_object=session)
