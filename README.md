django-twat
===========

A resuable [Django](http://www.djangoproject.com) application to read and display tweets.

django-twat uses the anonymous [Twitter API](http://dev.twitter.com) to pull a Twitter user's [timeline](http://dev.twitter.com/doc/get/statuses/user_timeline). The results are cached and stored in the Django context. These tweets are then accessible as a template variable.


Requirements
------------

* [pytz](http://pytz.sourceforge.net/) is used to convert the tweets' timestamps from UTC to the user's timezone.
* [simplejson](https://github.com/simplejson/simplejson) is used to read the JSON file returned by the Twitter API.


Installation
------------

1. Put the `twat` directory somewhere inside your Python path (like in your Django project folder).
2. Add `twat.context_processors.twitter` to your `settings.TEMPLATE_CONTEXT_PROCESSORS`.

  A good way to do this with overriding all of Django's default context processors is to first import the variable from the global settings and then append to it:

        from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

        TEMPLATE_CONTEXT_PROCESSORS += (
            'twat.context_processors.twitter',
        )


### Optional

If you want to take advantage of django-twat's default template, add `twat` to your `settings.INSTALLED_APPS`.


Usage
-----

After installing, the `tweets` variable will be available to all templates. This is a dictionary containing tweets and all the associated information returned by the Twitter API. Any URLs contained in the tweet will have been made into links, and any @usernames will have been turned into links to that user's Twitter profile. The timestamp for each tweet in the dictionary has been translated to a Python `datetime` object and converted to the users timezone (as defined by `settings.TIME_ZONE`).

If you have added `twat` to your `settings.INSTALLED_APPS`, django-twat's default template will be available for use. This outputs the tweets in an ordered list with a stylized (Twitter-like) timestamp. To use it, simply include the template in your desired location.

    {% include 'twat/tweets.html' %}


Settings
--------

django-twat includes a few settings that you may define in your project's main `settings` file.

### `TWITTER_USER`

The name of the Twitter user who's tweets you want to pull. This defaults to `None` and so must be defined before use.


### `TWITTER_NUMTWEETS`

The number of tweets that you want to pull. This defaults to 20. Note that the maximum that Twitter allows is 3200.

### `TWITTER_TIMEOUT`

For how many seconds should the tweets be stored in the cache. This defaults to 3 minutes. Currently [Twitter allows 150 requests per hour](http://dev.twitter.com/pages/rate-limiting#rest) for anonymous calls. Do not decrease the timeout setting to a point where django-twat is making more than 150 calls to the API per hour. Doing so will result in an HTTP 400 error.
