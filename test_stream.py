import datetime
import logging
import requests

STREAM_NUMBER = 1  # TODO: change this for second run

logger = logging.getLogger(__name__)
logging.basicConfig(**dict(
    format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s',
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler(filename=f"logs/stream{STREAM_NUMBER}.log", encoding='utf-8'),
        logging.StreamHandler(),
    ],
))

logger.info('Started downloading content')

# NOTE: Uncomment to check how SYNC view works
# r = requests.get('http://localhost:8000/sse', stream=True)

# NOTE: To check how ASYNC view works
r = requests.get('http://localhost:8000/sse_async', stream=True)

r.raise_for_status()

local_filename = f'logs/test_stream_data{STREAM_NUMBER}.txt'
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
