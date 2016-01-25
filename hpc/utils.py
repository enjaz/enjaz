# -*- coding: utf-8  -*-
import urllib2

def is_research_committee_member(user):
    return user.memberships.current_year().filter(english_name="Research Committee of the HPC").exists()

def is_organizing_committee_member(user):
    return user.memberships.current_year().filter(english_name="Organizing Committee of the HPC").exists()

def register_in_vma(session, registration):
    en_full_name = urllib2.quote(registration.get_en_full_name().replace(u'\u202a', '')
                                                                .replace(u'\u202b', '')
                                                                .replace(u'\u202c', '')
                                                                .replace(u'\u202d', '')
                                                                .encode("utf-8"))
    phone = registration.get_phone().replace(u'٠', '0')\
                                    .replace(u'١', '1')\
                                    .replace(u'٢', '2')\
                                    .replace(u'٣', '3')\
                                    .replace(u'٤', '4')\
                                    .replace(u'٥', '5')\
                                    .replace(u'٦', '6')\
                                    .replace(u'٧', '7')\
                                    .replace(u'٨', '8')\
                                    .replace(u'٩', '9')\
                                    .replace(u'\u202a', '')\
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
