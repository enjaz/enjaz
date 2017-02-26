import twitter
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Tweet

class Command(BaseCommand):
    help = "Send out tweets."

    def handle(self, *args, **options):
        for tweet in Tweet.objects.filter(was_sent=False, failed_trials__lte=5):
            if tweet.user:
                user_tokens = tweet.user.social_auth.all()[0].tokens
                access_token =  user_tokens['oauth_token']
                access_token_secret = user_tokens['oauth_token_secret']
            elif tweet.access:
                access_token = tweet.access.access_token
                access_token_secret = tweet.access.access_token_secret
            api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                              consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                              access_token_key=access_token,
                              access_token_secret=access_token_secret,)
            try:
                if tweet.media_path:
                    status = api.PostUpdate(tweet.text, media=tweet.media_path)
                else:
                    status = api.PostUpdate(tweet.text)
            except twitter.TwitterError, e:
                print "Something went wrong with #{}: ".format(tweet.pk), e
                tweet.failed_trials += 1
                tweet.save()
                continue

            tweet.tweet_id = status.id
            tweet.was_sent = True
            tweet.save()
