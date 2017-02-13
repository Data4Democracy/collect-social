from collect_social import config
import json


def process_content(batch):

    if 'file' in config.storage.keys():
        file_path = config.storage['file']

        with open(file_path, 'a') as f:
            for item in batch:
                json.dump(item._json, f)
                f.write('\n')
                print(item.text)
