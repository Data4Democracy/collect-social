
import json

## backend setup class?

async def process_batch(batch):

    with open('out_data.json', 'a') as f:
        f.writelines([json.dumps(item._json) + ',\n' for item in batch])
