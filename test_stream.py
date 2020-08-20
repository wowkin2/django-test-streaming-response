import datetime
import logging
import requests

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
                    level=logging.INFO)

logger.info('Started downloading content')

# Uncomment to check how sync view works
# r = requests.get('http://localhost:8000/sse', stream=True)

# To check how async view works
r = requests.get('http://localhost:8000/sse_async', stream=True)

r.raise_for_status()

local_filename = 'test_stream_data.txt'
logger.info('Opened file for writing')
with open(local_filename, 'wb') as f:
    logger.info('Iterating over content chunks')
    for chunk in r.iter_content(chunk_size=24):
        # If you have chunk encoded response uncomment if
        # and set chunk_size parameter to None.
        # if chunk:
        logger.info('Got chunk, writing to file')
        f.write((str(datetime.datetime.now()) + ' - ' + chunk.decode() + '\n').encode())
        logger.info('Wrote chunk to file')
    logger.info('Done')
