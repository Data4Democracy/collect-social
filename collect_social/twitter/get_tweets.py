from __future__ import print_function

import dataset
import time


def get_tweets(api, user_id, max_id=None):
    kwargs = {
        'user_id': user_id,
        'count': 200
    }

    if max_id is not None:
        kwargs['max_id'] = max_id

    try:
        tweets = api.GetUserTimeline(**kwargs)
    except Exception as e:
        print(kwargs)
        print(e)
        return []
    return tweets


def map_user_mention(db, tweet):
    for user_mention in tweet.user_mentions:
        mention_table = db['mention']

        um_data = {
            'user_id': tweet.user.id,
            'user_screen_name': tweet.user.screen_name,
            'tweet_id': tweet.id,
            'mentioned_user_id': user_mention.id,
            'mentioned_user_screen_name': user_mention.screen_name,
            'mentioned_tweet_id': None,
            'mention_type': 'mention'
        }

        if tweet.retweeted_status is not None and \
                        tweet.retweeted_status.user.screen_name == user_mention.screen_name:
            um_data['mention_type'] = 'retweet'
            um_data['mentioned_tweet_id'] = tweet.retweeted_status.id

        if tweet.in_reply_to_screen_name == user_mention.screen_name:
            um_data['mention_type'] = 'reply'
            um_data['mentioned_tweet_id'] = tweet.in_reply_to_status_id

        mention_table.upsert(
            um_data, ['tweet_id', 'user_id', 'mentioned_user_id'])


def map_media(db, tweet):
    media_table = db['media']

    for media in tweet.media:
        m_data = {
            'user_id': tweet.user.id,
            'user_screen_name': tweet.user.screen_name,
            'tweet_id': tweet.id,
            'media_type': media.type,
            'url': media.media_url
        }
        media_table.upsert(m_data, ['tweet_id', 'user_id', 'url'])


def map_hashtag(db, tweet):
    hashtag_table = db['hashtag']

    for hashtag in tweet.hashtags:
        h_data = {
            'user_id': tweet.user.id,
            'user_screen_name': tweet.user.screen_name,
            'tweet_id': tweet.id,
            'text': hashtag.text,
        }
        hashtag_table.upsert(h_data, ['tweet_id', 'user_id', 'text'])


def map_url(db, tweet):
    url_table = db['url']

    for url in tweet.urls:
        u_data = {
            'user_id': tweet.user.id,
            'user_screen_name': tweet.user.screen_name,
            'tweet_id': tweet.id,
            'url': url.expanded_url,
        }
        url_table.upsert(u_data, ['tweet_id', 'user_id', 'url'])


def process_tweet(db, tweet):
    # TODO breakup further

    tweet_table = db['tweet']
    tweet_type = 'tweet'
    referenced_tweet_id = None
    if tweet.retweeted_status is not None:
        tweet_type = 'retweet'
        referenced_tweet_id = tweet.retweeted_status.id
    elif tweet.in_reply_to_status_id is not None:
        tweet_type = 'reply'
        referenced_tweet_id = tweet.in_reply_to_status_id

    t_data = {
        'tweet_id': tweet.id,
        'user_id': tweet.user.id,
        'user_screen_name': tweet.user.screen_name,
        'tweet_type': tweet_type,
        'referenced_tweet_id': referenced_tweet_id
    }

    if tweet.geo is not None and 'coordinates' in tweet.geo:
        t_data['latitude'] = tweet.geo['coordinates'][0]
        t_data['longitude'] = tweet.geo['coordinates'][1]

    tweet_props = [
        'created_at',
        'favorite_count',
        'favorited',
        'lang',
        'retweet_count',
        'retweeted',
        'source',
        'text'
    ]

    for key in tweet_props:
        t_data[key] = getattr(tweet, key)

    tweet_table.upsert(t_data, ['tweet_id'])


def map_tweet_attributes(db, tweet):
    map_user_mention(db, tweet)

    if tweet.media:
        map_media(db, tweet)

    if tweet.hashtags:
        map_hashtag(db, tweet)

    if tweet.urls:
        map_url(db, tweet)


def upsert_tweets(db, tweets):
    if not tweets:
        return None

    for tweet in tweets:
        map_tweet_attributes(db, tweet)
        process_tweet(db, tweet)


def update_user(db, user_id, collected=True, suspended=False):
    user_table = db['user']
    result = None

    if collected and not suspended:
        update_dict = dict(user_id=user_id, tweets_collected=1)
        result = user_table.update(update_dict, ['user_id'])

    elif collected and suspended:
        update_dict = dict(user_id=user_id,
                           tweets_collected=1, is_suspended=1)
        result = user_table.update(update_dict, ['user_id'])

    elif suspended:
        update_dict = dict(user_id=user_id, is_suspended=1)
        result = user_table.update(update_dict, ['user_id'])

    if not result:
        print("Could not update {} to collected: {} and suspended: {}".format(
            user_id, collected, suspended))
    return result


def run(api, connection_string, user_id=None, all_tweets=True):

    db = dataset.connect(connection_string)
    user_table = db['user']

    if not user_id:
        users = user_table.find(tweets_collected=0)
        user_ids = [u['user_id'] for u in users]
    else:
        user_ids = []

    if user_id:
        request_limit = 16  # 200 tweets per request
        max_id = None
        while True:
            tweets = get_tweets(api, user_id, max_id=max_id)

            tweet_ids = [tweet.id for tweet in tweets]
            if len(tweet_ids) > 0:
                max_id = min(tweet_ids)
                upsert_tweets(db, tweets)

            if len(tweets) < 200:
                update_user(db, user_id, collected=True)
                break

            request_limit -= 1
            if request_limit <= 0:
                print('Request limit hit')
                break
            print(str(request_limit) + ' requests to go')

            time.sleep(1)

    remaining = len(user_ids)
    for user_id in user_ids:
        print(str(remaining) + ' users to go')

        if all_tweets:
            max_id = None

            for i in range(16):
                tweets = get_tweets(api, user_id, max_id=max_id)
                tweet_ids = [tweet.id for tweet in tweets]
                if len(tweet_ids) > 0:
                    max_id = min([tweet.id for tweet in tweets])
                    upsert_tweets(db, tweets)

                print('Got ' + str(i) + ' iteration of tweets for ' + str(user_id))
                time.sleep(1)
            update_user(db, user_id, collected=True)
        else:
            tweets = get_tweets(api, user_id)
            upsert_tweets(db, tweets)
            if len(tweets) == 0:
                update_user(db, user_id, collected=True, suspended=True)

        remaining -= 1
        time.sleep(1)
