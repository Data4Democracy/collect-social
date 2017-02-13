import tweepy
from collect_social.backend import process
# from collect_social.backend import backend


class StreamListener(tweepy.StreamListener):
    def __init__(self, per_batch=10, batch_limit=3):
        super(StreamListener, self).__init__()
        self.counter = 0
        self.per_batch = per_batch
        self.batch_limit = batch_limit
        self.tweet_batch = []
        self.batch_counter = 0
        # self.backend = backend.Setup()

    def on_status(self, status):
        self.counter += 1
        self.tweet_batch.append(status)
        print(self.counter)

        # TODO if eventendator >  send_to_eventadaor(status)

        if self.counter >= self.per_batch:

            # can we do this async?
            process.process_batch(self.tweet_batch)
            self.tweet_batch = []
            self.batch_counter += 1
            self.counter = 0

        # Max batches reached
        if self.batch_limit and self.batch_counter >= self.batch_limit:
            print('batch limit {} hit'.format(self.batch_counter))
            return False

    def on_error(self, status_code):
        pass


def start_stream(topics, creds):
    auth = tweepy.OAuthHandler(creds['c_key'], creds['c_secret'])
    auth.set_access_token(creds['a_token'], creds['a_token_secret'])
    api = tweepy.API(auth)

    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=topics)
