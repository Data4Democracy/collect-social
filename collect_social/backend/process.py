from collect_social import config
import json

## backend setup class? 


def process_batch(batch):

    if 'file' in config.storage.keys():
        file_path = config.storage['file']

        with open(file_path, 'a') as f:
            for item in batch:
                json.dump(item._json, f)
                f.write('\n')
                print(item.text)

    # if 's3' in config.storage.keys():
        # set aws creds
        # upload data

    # if sqlite  in storage -- allows for multiple backends
        # insert (batch)
