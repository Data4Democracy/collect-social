# WIP progress config file. Will use different process later
import os

twitter_terms = ['flynn', 'trump', 'russia']

twitter_config = {
    'access_token': '',
    'access_token_secret': '',
    'consumer_key': '',
    'consumer_secret': '',

    'twitter_terms': twitter_terms,
    'batches': 3,  # -1 will stream indefinitely
    'per_batch': 10
}

# Eventador
ev_config = {
    'broker':'',
    'topic': b''  # pykafka wants bytestrings here
}

# not used for now
storage = {
            # 's3': {'bucket': bucket, 'credentials': credentials, 'format': 'JSON'}
            'file': os.path.join(os.getcwd(), 'output_example.json')
}

config = {**twitter_config, **ev_config, **storage}
