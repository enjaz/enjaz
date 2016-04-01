# -*- coding: utf-8  -*-
import urllib2
import json
from post_office import mail

from django.http import HttpResponseRedirect
from django.utils import timezone

from core.utils import hindi_to_arabic
from events.models import Event


def is_organizing_committee_member(user, event):
    organizing_club = event.organizing_club
    return user.memberships.current_year().filter(pk=organizing_club.pk).exists()

def check_if_closed(event):
    if event.registration_closing_date and \
       timezone.now() > event.registration_closing_date:
        return HttpResponseRedirect(reverse('events:registration_closed'))

def get_user_organizing_events(user):
    user_events = (Event.objects.filter(organizing_club__members=user) | \
                   Event.objects.filter(organizing_club__coordinator=user) | \
                   Event.objects.filter(organizing_club__deputies=user)).distinct()
    return user_events

def register_in_vma(session, registration):
    en_full_name = urllib2.quote(registration.get_en_full_name().replace(u'\u202a', '')
                                                                .replace(u'\u202b', '')
                                                                .replace(u'\u202c', '')
                                                                .replace(u'\u202d', '')
                                                                .encode("utf-8"))
    arabic_phone_number = hindi_to_arabic(registration.get_phone())
    phone_number = arabic_phone_number.replace(u'\u202a', '')\
                                      .replace(u'\u202b', '')\
                                      .replace(u'\u202c', '')\
                                      .replace(u'\u202d', '')\
                                      .replace(u'\xa0', '')\
                                      .replace(' ', '')\
                                      .replace('+', '')\
                                      .encode("utf-8")

    email = urllib2.quote(registration.get_email())

    if session.vma_time_code:
        url = u"http://www.medicalacademy.org/portal/register/member/workshop/organizer?workshop_id={}&workshop_time_code={}&organizer=1&full_name={}&email={}&mobile={}".format(session.vma_id, session.vma_time_code, en_full_name, email, phone).encode("utf-8")
    else:
        url = u"http://www.medicalacademy.org/portal/register/member/event/organizer?event_id={}&organizer=1&full_name={}&email={}&mobile={}".format(session.vma_id, en_full_name, email, phone).encode("utf-8")

    response = urllib2.urlopen(url).read()

    if response == 'true':
        registration.moved_sessions.add(session)
    else:
        print "response was", response


def send_onsite_confirmation(registration):
    programs = []
    for session in registration.moved_sessions.all():
        url = "http://medicalacademy.org/portal/list/registration/get/data?event_id=" + str(session.vma_id)
        data = urllib2.urlopen(url)
        processed_data = json.load(data)

        for user in processed_data:
            if user['email'].lower() == registration.get_email().lower():
                programs.append((session, user['confirmation_link']))
                break

    email_context = {'registration': registration,
                     'programs': programs}

    mail.send([registration.get_email()],
               template="hpc_registration_confirmed",
               context=email_context)
    registration.confirmation_sent = True
    registration.save()
