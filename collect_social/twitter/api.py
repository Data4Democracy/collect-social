import datetime
import tweepy
from collect_social import config


# def map_location(twitter_user):
#     # TODO Location is user entered, will have to consider parsing in post processing
#     location = {
#         'raw_location': None if twitter_user.location is None else twitter_user.location,
#         'timezone': None if twitter_user.time_zone is None else twitter_user.time_zone
#     }
#     return location
#
#
# def twitter_engagement(twitter_user):
#     """Twitter engagement is status updates + favorites"""
#     try:
#         favorite_count = int(twitter_user.favourites_count)
#         status_updates = int(twitter_user.statuses_count)
#         engagement = favorite_count + status_updates
#     except Exception as e:
#         print(e)
#         engagement = None
#
#     return engagement
#
#
# def check_original_content(status):
#     # assume it is not reply/quote
#     content_type, orig_id, orig_content = None, None, None
#
#     # check if quote
#     if hasattr(status, 'quoted_status_id'):
#         content_type = 'quote'
#         orig_id = status.quoted_status_id
#         orig_content = status.quoted_status['text']
#
#     # check if reply
#     # API returns "Null" if not reply. Tweepy status always hasattr in_reply_to_user_id
#     if status.in_reply_to_user_id is not None:
#         content_type = 'reply'
#         orig_id = status.in_reply_to_user_id
#         # orig_content N/A for replies
#
#     return content_type, orig_id, orig_content
#
#
# def map_asset(kind, location):
#     """Create asset"""
#     asset_types = ['href', 's3', 'db']
#     if kind in asset_types:
#         asset = {
#             'kind': kind,
#             'location': location
#         }
#     else:
#         raise ValueError('Unrecognized type {}'.format(kind))
#
#     return asset
#
#
# def map_user(twitter_user):
#     """
#     :param twitter_user:
#     :return: user dict
#     """
#
#     user = {
#         'platform': 'twitter',
#         'user_name': twitter_user.screen_name,
#         'display_name': twitter_user.name,
#         'post_count': twitter_user.statuses_count,
#         'user_id': twitter_user.id_str,
#         'avatar': map_asset('href', twitter_user.profile_image_url),
#         'bio': twitter_user.description,
#         'location': map_location(twitter_user),
#         'user_created': twitter_user.created_at.isoformat(),
#         'updated': datetime.datetime.utcnow().isoformat(),
#         'follower': twitter_user.followers_count,
#         'following': twitter_user.friends_count,
#         'is_verified': twitter_user.verified,
#         'engagement': twitter_engagement(twitter_user)
#     }
#     return user
#
#
# def map_users(twitter_users):
#     return [map_user(user) for user in twitter_users]
#
#
# def map_following(twitter_following):
#     # return d4d.Following
#     pass
#
#
# def map_content_meta(entities):
#     content_meta = {}
#
#     if entities:
#         if len(entities['hashtags']) > 0:
#             hashtags = [h['text'] for h in entities['hashtags']]
#             content_meta['hashtags'] = hashtags
#         if len(entities['urls']) > 0:
#             urls = [url['url'] for url in entities['urls']]
#             content_meta['url'] = urls
#         if len(entities['user_mentions']) > 0:
#             user_mentions = [user['id'] for user in entities['user_mentions']]
#             content_meta['user_mentions'] = user_mentions
#     return content_meta
#
#
# def map_post(twitter_post):
#     content_type, orig_content_id, orig_content = check_original_content(twitter_post)
#
#     return {
#             'platform': 'twitter',
#             'source': 'placeholder', # TODO
#             'user_name': twitter_post.user.screen_name,
#             'user_id': twitter_post.user.id_str,
#             'user_platform': twitter_post.source,
#             'content_id': twitter_post.id,
#             'created_at': twitter_post.created_at.isoformat(),
#             'updated_at': datetime.datetime.utcnow().isoformat(),
#             'reply_type': None if content_type is None else content_type,
#             'original_content_id': None if orig_content_id is None else orig_content_id,
#             'original_content_text': None if orig_content is None else orig_content,
#             'text': twitter_post.text,
#             # media : ???
#             'reactions': map_reactions(twitter_post),
#             'location': map_location(twitter_post.user),
#             'meta': map_content_meta(twitter_post.entities)
#         }
#
#
# def map_posts(twitter_posts):
#     return [map_post(post) for post in twitter_posts]
#
#
# def map_reactions(twitter_post):
#     return {
#         'pos_sentiment': twitter_post.retweet_count + twitter_post.favorite_count,
#         # neg_sentiment N/A for twitter
#     }
#
#
# def map_reactions_native(twitter_post):
#     return {
#             'platform': 'twitter',
#             'retweet_count': twitter_post.retweet_count,
#             'favorite_count': twitter_post.favorite_count
#             }
#

class Twitter(object):
    """This class represents an authenticated twitter connection"""

    def __init__(self, consumer_key=config.consumer_key, consumer_secret=config.consumer_secret,
                 access_token=config.access_token, access_token_secret=config.access_token_secret):

        # read creds from config file for now
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
        pass

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

    def get_replies(self, post_id, native=False):
        """
        :param post_id: twitter tweet ID
        :param native: bool
            if true, append native tweet object to each post object
        :return: list of replies to post ID
        """
        # TODO Twitter does not offer clean solution to get replies

    def get_reaction(self, post_id, native=False):
        """
        :param post_id: twitter post ID
        :param native:
        :return: dict
        """
        twitter_post = self._api.get_status(post_id)

        return {
                'retweet_count': twitter_post.retweet_count,
                'favorite_count': twitter_post.favorite_count
        }
