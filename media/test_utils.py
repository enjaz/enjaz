"""
Utility functions for automated testing.
"""
import datetime
from django.utils import timezone
from media.models import Article, Poll, POLL_CHOICE_SEPARATOR, HUNDRED_SAYS, WHAT_IF, PollResponse

from clubs.utils import get_media_center
from clubs.test_utils import set_club_coordinator, add_club_member
from accounts.test_utils import create_user


def media_center_head(user):
    media_center = get_media_center()
    set_club_coordinator(media_center, user)
    return user

def media_center_member(user):
    media_center = get_media_center()
    add_club_member(media_center, user)
    return user

def create_article(author=create_user(),
                   title=("Test Article Title " + str(Article.objects.count() + 1)),
                   text="Test Article Text"):
    return Article.objects.create(author=author,
                                  title=title,
                                  text=text)

def create_articles(count):
    for i in range(count):
        create_article()


def create_poll(poll_type,
                title=("Test Poll Title " + str(Poll.objects.count() + 1)),
                text="Test Poll Text",
                choices=("Choice 1", "Choice 2", "Choice 3"),
                open_date=timezone.now(),
                close_date=(timezone.now() + datetime.timedelta(days=7)),
                creator=create_user()):

    poll =  Poll.objects.create(poll_type=poll_type,
                                title=title,
                                text=text,
                                choices=choices,
                                open_date=open_date,
                                close_date=close_date,
                                creator=creator)
    for choice in choices:
        poll.choices.create(value=choice)
    return poll


def create_poll_response(poll=create_poll(HUNDRED_SAYS),
                         user=create_user(),
                         choice="",
                         comment="COMMENT"):
    return PollResponse.objects.create(poll=poll,
                                       user=user,
                                       choice=choice,
                                       comment=comment)