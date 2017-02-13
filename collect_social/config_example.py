# WIP progress config file. Will use different process later
import os
consumer_key=''
consumer_secret=''

access_token=''
access_token_secret=''

#temp hack
path_to_file = os.path.join(os.getcwd(), 'output_example.json')


storage = {
            #'s3': {'bucket': bucket, 'credentials': credentials, 'format': 'JSON'}
            'file': path_to_file,
            # 'eventador': {eventador_config}
}
