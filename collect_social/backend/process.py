import config as cfg
import json


async def process_batch(batch):
    file_path = cfg.config['file']

    with open(file_path, 'a') as f:
        f.writelines([json.dumps(item._json) + ',\n' for item in batch])
        print([item.text + '\n' for item in batch])
