from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.utils import translation
import re

from certificates.models import Certificate
from events.models import Attendance, Event, Session, SessionRegistration
from post_office import mail
import accounts.utils

# Attendance rules:
#
# 1) The event certificate will require 5 sign-ins which can include
#    the general program, college programs and workshops.
#
# 2) The workshop and college program certificates will require both
#    sign-in and sign-out, except two ER and suturing workshops
#    (pk=53,54) which did not have accurate sign-in/sign-out process,
#    so we will mark those with either a sign-in or a sign out as
#    attendant.
# 
# 3) Those who attended the MBTI workshop (pk=43) will get the
#    conference certificate if they have sign-ins, sign-outs in both
#    days since it was a full-day workshop spanning two days.
#
# 4) Those who signed up for the cancelled pharmacy program will get
#    two extra attendances as they were not required to attend the
#    last and third day.

# April 23, 24
days = [23, 24]

# Session pks
colleges =  [78, 80, 81, 82, 83, 84]
workshops = range(38, 43) + range(44, 53) + range(55, 78)
inaccurate_workshops = [53, 54]
LONG_WORKSHOP_PK = 43
GENERAL_PROGRAM_PK = 20

# Attendance categories
all_categories = ["I", "M", "O", ""]
no_mid_categories = ["I", "O", ""]

sessions = {}
for pk in workshops + colleges + inaccurate_workshops + [LONG_WORKSHOP_PK] + [GENERAL_PROGRAM_PK]:
    sessions[pk] = Session.objects.get(pk=pk)

def generate_session_certificate(user, session_pk):
    session = sessions[session_pk]
    name = accounts.utils.get_user_en_full_name(user)
    if not name:
        name = user.username

    session_name = re.sub("[ -]*(:?fe)?male$", "", session.name, flags=re.I).strip()

    if Certificate.objects.filter(sessions__pk=session_pk, user=user).exists():
        print u"Skipping {} for {} as previously generated.".format(session_name, name)
        return
    else:
        print u"Preparing {} for {}.".format(session_name, name)
    scfhs_number = accounts.utils.get_user_scfhs_number(user)
    texts = [name, session_name, scfhs_number]

    session.certificate_template.generate_certificate(user, texts, content_object=session)

class Command(BaseCommand):
    help = "Generate HPC 2017 Certificates."

    def handle(self, *args, **options):
        translation.activate(settings.LANGUAGE_CODE)
        event = Event.objects.get(code_name="hpc2-r")
        from_email = event.get_notification_email()
        domain = Site.objects.get_current().domain
        url = "https://{}{}".format(domain,
                                    reverse('certificates:list_certificates_per_user'))

        for hpc_user in User.objects.filter(session_registrations__attendance__isnull=False,
                                            session_registrations__session__event__code_name="hpc2-r").distinct():
            user_total = 0
            long_workshop_positive = False

            # Check long workshop:
            count = 0
            # Check both April 23rd and April 24th
            for day in days:
                # One sign-in and one sign-out on April 23rd, and one sign-in
                # and one sign-out on April 24th (total of four) for the MBTI
                # workshop will give people two certificates: one for the
                # conference, the other of the MBTI workshop.
                for category in no_mid_categories:
                    if Attendance.objects.filter(session_registration__session__pk=LONG_WORKSHOP_PK,
                                                 session_registration__user=hpc_user,
                                                 date_submitted__day=day,
                                                 category=category).exists():
                        count += 1
            if count >= 4:
                generate_session_certificate(hpc_user, LONG_WORKSHOP_PK)
            elif count >= 1:
                user_total += count

            # Look into the General Progrram only if user has no long
            # workshop certificate.  Check both April 23rd and April
            # 24th.
            if not long_workshop_positive:
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
                count = 0
                for category in no_mid_categories:
                    if Attendance.objects.filter(session_registration__session__pk=pk,
                                                 session_registration__user=hpc_user,
                                                 category=category).exists():
                        count += 1
                if count >= 2:
                    user_total += 1
                    generate_session_certificate(hpc_user, pk)

            # Either a sign-in or a sign-out is enough for inaccurate workshops.
            for pk in inaccurate_workshops:
                if Attendance.objects.filter(session_registration__session__pk=pk,
                                             session_registration__user=hpc_user).exists():
                    user_total += 1
                    generate_session_certificate(hpc_user, pk)

            # Handle the pharmacy program:
            if not long_workshop_positive:
                if hpc_user.session_registrations.filter(session__pk=79,
                                                         is_deleted=False).exists():
                    user_total += 2
            if user_total >= 5 or long_workshop_positive:
                name = accounts.utils.get_user_en_full_name(hpc_user)
                if not name:
                    name = user.username
                scfhs_number = accounts.utils.get_user_scfhs_number(hpc_user)
                texts = [name, scfhs_number]
                session = sessions[GENERAL_PROGRAM_PK]
                if Certificate.objects.filter(sessions__pk=GENERAL_PROGRAM_PK, user=hpc_user).exists():
                    print u"Skipping {} for {} as previously generated.".format(session.name, name)
                    continue
                else:
                    print u"Preparing {} for {}.".format(session.name, name)
                session.event.event_certificate_template.generate_certificate(hpc_user, texts, content_object=session)
