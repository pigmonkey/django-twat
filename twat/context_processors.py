import simplejson
import re
from urllib2 import urlopen
from datetime import datetime

from pytz import timezone
from django.core.cache import cache
from django.utils.html import urlize
from django.conf import settings

from twat import settings as twat_settings


def twitter(request):
    """Return the most recent tweets for a user."""
    # Check the cache for tweets. If they exist, return them.
    tweets = cache.get('tweets')
    if tweets:
        return {'tweets': tweets}

    # Pull the tweets from the Twitter API in JSON format.
    url = 'http://api.twitter.com/1/statuses/user_timeline/%s.json?count=%i' %\
          (twat_settings.TWITTER_USER, twat_settings.TWITTER_NUMTWEETS)
    page = urlopen(url)
    timeline = simplejson.loads(page.read())

    for tweet in timeline:
        # Convert the tweet's created time to a datetime object.
        tweet['created_at'] = datetime.strptime(tweet['created_at'],
                                                "%a %b %d %H:%M:%S +0000 %Y")

        # Convert the datetime from a naive object to an aware one.
        tweet['created_at'] = tweet['created_at'].replace(tzinfo=timezone('UTC'))

        # Convert the datetime object's timezone to local time.
        tweet['created_at'] = tweet['created_at'].astimezone(timezone(settings.TIME_ZONE))

        # Build a permlink for the tweet.
        tweet['permalink'] = 'https://twitter.com/%s/status/%s' %\
                              (twat_settings.TWITTER_USER, tweet['id'])

        # Turn any URLs in the tweets into links. This must be done before
        # linking Twitter usernames, as urlize() expects a string without any
        # HTML markup.
        tweet['text'] = urlize(tweet['text'], nofollow=True)

        # Find any usernames and make them links.
        twitter_username_re = re.compile(r'@([A-Za-z0-9_]+)')
        tweet['text'] = twitter_username_re.sub(
                                    lambda m:
                                    '<a href="http://twitter.com/%s">%s</a>' %\
                                    (m.group(1), m.group(0)), tweet['text'])

    # Add the tweets to the cache
    cache.set('tweets', timeline, twat_settings.TWITTER_TIMEOUT)

    # Return the tweets
    return{'tweets': timeline}
