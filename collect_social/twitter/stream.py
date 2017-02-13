import tweepy


class StreamListener(tweepy.StreamListener):
    def __init__(self):
        super(StreamListener, self).__init__()
        self.counter = 0
        self.limit = 10

    def on_status(self, status):
        self.counter += 1
        if self.counter >= self.limit:
            return False
        else:
            print(status.text)

    def on_error(self, status_code):
        pass


def start_stream(topics, creds):
    auth = tweepy.OAuthHandler(creds['c_key'], creds['c_secret'])
    auth.set_access_token(creds['a_token'], creds['a_token_secret'])
    api = tweepy.API(auth)

    stream_listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
    stream.filter(track=topics)
