"""
Utility functions for automated testing.
"""
from .models import Article

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