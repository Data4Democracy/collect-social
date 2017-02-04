import tweepy

def map_user(twitter_user):
    # return d4d.User
    pass

def map_followers(twitter_followers):
    # return d4d.Followers
    pass

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
    def __init__(self, app_key=None, app_secret=None,
                 consumer_key=None, consumer_secret=None):
        # Default creds to some config module/file/etc
        self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self._auth.set_access_token(app_key, app_secret)
        self._api = tweepy.API(self._auth)

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
        pass

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
        pass

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
