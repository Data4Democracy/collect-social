import config_example as cfg
import json


async def process_batch(batch):
    file_path = cfg.config.get('file', None)
    if file_path:
        with open(file_path, 'a') as f:
            f.writelines([json.dumps(item._json) + ',\n' for item in batch])
