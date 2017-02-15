import tweepy
from collect_social.backend import process
from collect_social.backend.eventador import EventadorClient
from collect_social import config_example
import asyncio
import time
# from collect_social.backend import backend


class StreamListener(tweepy.StreamListener):
    def __init__(self, eventador, per_batch=10, batch_limit=3):
        super(StreamListener, self).__init__()
        self.batch_counter = 0
        self.per_batch = per_batch
        self.batch_limit = batch_limit
        self.eventador = eventador
        self.init_batch()
        # self.backend = backend.Setup()

    def on_status(self, status):
        self.counter += 1
        self.tweet_batch.append(status)

        if self.counter >= self.per_batch:
            self.process_tasks()
        if self.batch_limit and self.batch_counter >= self.batch_limit:         # Max batches reached
            return False

    def process_tasks(self):
        loop = asyncio.get_event_loop()
        messages = [{'key': bytes(n), 'value': tweet._json} for n, tweet in enumerate(self.tweet_batch)]
        tasks = [
            loop.create_task(process.process_batch(self.tweet_batch)),
            loop.create_task(self.eventador.produce_many(messages))
        ]

        loop.run_until_complete(asyncio.gather(*tasks))
        self.increment_batch()
        self.init_batch()

    def increment_batch(self):
        self.batch_counter += 1
        print("Batch #%s completed %s statuses collected" % (self.batch_counter, self.counter))

    def init_batch(self):
        self.tweet_batch = []
        self.counter = 0

    def on_error(self, status_code):
        pass


class CollectSocialTwitterListener:
    def __init__(self, config):
        self.config = config
        self.twitter_terms = config.get('twitter_terms')
        self.eventador = EventadorClient(config)
        self.tweepy_listener = StreamListener(self.eventador)

    def handle_api_auth(self):
        auth = tweepy.OAuthHandler(self.config['consumer_key'], self.config['consumer_secret'])
        auth.set_access_token(self.config['access_token'], self.config['access_token_secret'])
        return tweepy.API(auth).auth

    def start_stream(self, get_performance=False):
        start = time.time()

        stream = tweepy.Stream(auth=self.handle_api_auth(), listener=self.tweepy_listener)
        stream.filter(track=self.twitter_terms)

        if get_performance:
            print("Total Execution Time: %s seconds" % (time.time() - start))


CollectSocialTwitterListener(config_example.config).start_stream(True)
