import twitter
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Tweet

class Command(BaseCommand):
    help = "Send out tweets."

    def handle(self, *args, **options):
        for tweet in Tweet.objects.filter(was_sent=False, failed_trails__lte=5):
            user_tokens = tweet.user.social_auth.all()[0].tokens
            api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                              consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                              access_token_key=user_tokens['oauth_token'],
                              access_token_secret=user_tokens['oauth_token_secret'],)
            try:
                if tweet.media_path:
                    status = api.PostMedia(tweet.text, tweet.media_path)
                else:
                    status = api.PostUpdate(tweet.text)
            except twitter.TwitterError, e:
                print "Something went wrong with #{}: ".format(tweet.pk), e
                tweet.failed_trails += 1
                tweet.save()
                continue

            tweet.tweet_id = status.id
            tweet.was_sent = True
            tweet.save()
