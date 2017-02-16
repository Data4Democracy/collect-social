import tweepy
from collect_social.backend import process
from collect_social.backend.eventador import EventadorClient
import asyncio
import time


class StreamListener(tweepy.StreamListener):
    def __init__(self, eventador, per_batch, batch_limit):
        super(StreamListener, self).__init__()
        self.batch_counter = 0
        self.per_batch = per_batch
        self.batch_limit = batch_limit
        self.eventador = eventador
        self.init_batch()

    def on_status(self, status):
        self.counter += 1
        self.tweet_batch.append(status)

        if self.batch_limit == -1:
            if self.counter >= self.per_batch:
                self.process_tasks()

        else:
            if self.counter >= self.per_batch:
                self.process_tasks()
            elif self.batch_limit and self.batch_counter >= self.batch_limit:         # Max batches reached
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
    def __init__(self, config, auth):
        self.config = config
        self.twitter_terms = config.get('twitter_terms')
        self.eventador = EventadorClient(config)
        self.tweepy_listener = StreamListener(
            self.eventador,
            config.get('per_batch', 10),
            config.get('batches', 3))
        self.auth = auth

    def start_stream(self, topics=None, stats=False):
        start = time.time()

        if topics is not None:
            # override topics to track if topics param provided
            track = topics
        else:
            # fallback to settings
            track = self.twitter_terms

        stream = tweepy.Stream(auth=self.auth, listener=self.tweepy_listener)

        # temporary until logging implemented
        print('--Twitter Stream--\nBatch limit: {}\nTweets Per Batch: {}\nTracking Topics: {}'.format(
                self.tweepy_listener.batch_limit, self.tweepy_listener.per_batch,
                track))
        stream.filter(track=track)

        if stats:
            print("Total Execution Time: %s seconds" % (time.time() - start))
