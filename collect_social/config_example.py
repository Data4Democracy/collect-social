# WIP progress config file. Will use different process later
import os

twitter_config = {
    'access_token': '',
    'access_token_secret': '',
    'consumer_key': '',
    'consumer_secret': '',

    'twitter_terms': ['flynn', 'trump', 'russia']
}

#Eventador
ev_config = {
    'broker':'',
    'topic': b'' # pykafka wants bytestrings here
}

storage = {
            #'s3': {'bucket': bucket, 'credentials': credentials, 'format': 'JSON'}
            'file': os.path.join(os.getcwd(), 'output_example.json')
}


config = { **twitter_config, **ev_config, **storage}
