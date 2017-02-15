from collect_social import config_example
import json

## backend setup class? 

async def process_batch(batch):

    config = config_example.config
    if 'file' in config.keys():
        file_path = config['file']

        with open(file_path, 'a') as f:
            f.writelines([json.dumps(item._json) + ',\n' for item in batch])

    # if 's3' in config.storage.keys():
        # set aws creds
        # upload data

    # if sqlite  in storage -- allows for multiple backends
        # insert (batch)
