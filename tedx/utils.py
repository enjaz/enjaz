# -*- coding: utf-8  -*-
from core.models import Tweet

def create_tweet(user):
    if not user.social_auth.exists():
        return
    
    Tweet.objects.create(text="سجّلت في @TEDxKSAUHS الذي سيقام يوم السبت 15 أبريل!  يمكن التسجيل من هنا:\nhttps://tedxksauhs.com\n#TEDxKSAUHS",
                         user=user)
