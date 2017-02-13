import tweepy
from collect_social import config
from collect_social.twitter import stream


class Twitter(object):
    """This class represents an authenticated twitter connection"""

    def __init__(self, consumer_key=config.consumer_key, consumer_secret=config.consumer_secret,
                 access_token=config.access_token, access_token_secret=config.access_token_secret):

        # read creds from config file for now
        self._credentials = {'c_key': consumer_key, 'c_secret': consumer_secret,
                             'a_token': access_token, 'a_token_secret': access_token_secret}
        self._auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self._auth.set_access_token(access_token, access_token_secret)
        self._api = tweepy.API(self._auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


    def get_post(self, post_id):
        """
        Params: id
        Returns: dict
        """
        return self._api.get_status(post_id)

    def get_posts(self, user_id):
        """
        Params: id
        Returns: dict[ ]
        """
    # NOTE: will download all non-retweets of the past 3200 posts
    # from user_id
        posts = []
        for page in tweepy.Cursor(self._api.user_timeline, id=user_id).pages():
            posts.extend(page)

        return posts

    def get_user(self, handle, native=False):
        """
        Sends get user request

        :param handle: user handle
        :param native: appened native content flag
        :return: dict
        """

        return self._api.get_user(handle)


    def get_users(self, id_list):
        """
        Params: id[ ]
        Returns: dict[ ]
        """
        users = []
        for user in id_list:
            users.append(self.get_user(user))
        return users


    def get_followers(self, user_id):
        """
        Params: id
        Returns: dict[ ]
        """
        followers = []
        for page in tweepy.Cursor(self._api.followers, id=user_id).pages():
            followers.extend(page)

        return followers

    def get_following(self, user_id):
        """
        Params: id
        Returns: dict[ ]
        """
        following = []
        for page in tweepy.Cursor(self._api.friends, user_id).pages():
            following.extend(page)

        return following

    def get_replies(self, post_id):
        """
        :param post_id: twitter tweet ID
        :param native: bool
            if true, append native tweet object to each post object
        :return: list of replies to post ID
        """
        # TODO Twitter does not offer clean solution to get replies

    def get_reaction(self, post_id):
        """
        :param post_id: twitter post ID
        :param native:
        :return: dict
        """

        twitter_post = self.get_post(post_id)

        return {
                'retweet_count': twitter_post.retweet_count,
                'favorite_count': twitter_post.favorite_count
        }

    def start_stream(self, topics):
        stream.start_stream(topics=topics, creds=self._credentials)
