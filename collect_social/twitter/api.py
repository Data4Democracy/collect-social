import tweepy


def map_user(twitter_user):
    return {
        'screen_name': twitter_user.screen_name,
        'display_name': twitter_user.name,
        'user_id': twitter_user.id_str,
        'description': twitter_user.description,
        'language': twitter_user.lang,
        'location': twitter_user.location,
        'timezone': twitter_user.time_zone,
        'user_created': twitter_user.created_at,
        'followers_count': twitter_user.followers_count,
        'friends_count': twitter_user.friends_count,
        'status_count': twitter_user.statuses_count,
        'favorites_count': twitter_user.favourites_count,
        'is_verified': twitter_user.verified
    }


def map_followers(twitter_followers):
    return [map_user(follower) for follower in twitter_followers]


def map_following(twitter_following):
    # return d4d.Following
    pass


def map_post(twitter_post):
    # return d4d.Post
    pass


def map_comment(twitter_post):
    # return d4d.Comment
    pass


def map_reactions(twitter_post):
    # return d4d.Reactions
    pass


class Twitter(object):
    def __init__(self, consumer_key=None,consumer_secret=None,
                 access_token=None, access_token_secret=None):
        # Default creds to some config module/file/etc
        self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self._auth.set_access_token(access_token, access_token_secret)
        self._api = tweepy.API(self._auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def get_post(self, id):
        """
        Params: id
        Returns: dict
        """
        pass

    def get_posts(self, user_id):
        """
        Params: id[ ]
        Returns: dict[ ]
        """
        pass

    def get_user(self, handle):
        """
        Params: id
        Returns: dict
        """
        tweepy_user = self._api.get_user(handle)
        return map_user(tweepy_user)

    def get_users(self, id_list):
        """
        Params: id[ ]
        Returns: dict[ ]
        """
        pass

    def get_followers(self, user_id):
        """
        Params: id
        Returns: dict[ ]
        """
        followers = []
        for page in tweepy.Cursor(self._api.followers, id=user_id).pages():
            followers.extend(page)

        return map_followers(followers)

    def get_following(self, user_id):
        """
        Params: id
        Returns: dict[ ]
        """

    def get_comments(self, post_id):
        """
        Params: id
        Returns: dict[ ]
        """
        pass

    def get_reactions(self, post_id):
        """
        Params: id
        Returns: dict[ ]
        """
        pass
