import asyncio
import logging
import time

from django.http import StreamingHttpResponse
from base.sse import SSEResponse as SSE


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s', level=logging.INFO)


LINE_LENGTH = 24
N_CHUNKS = 10
CONTENT_SIZE = int(2 ** 16 / LINE_LENGTH) * N_CHUNKS
TIME_SLEEP = 0.001

logger.info(f'Configured: '
            f'CONTENT_SIZE={CONTENT_SIZE}, LINE_LENGTH={LINE_LENGTH}, '
            f'N_CHUNKS={N_CHUNKS}, TIME_SLEEP={TIME_SLEEP}')


def gen_message(msg):
    logger.info('Generated message for iteration: %s', msg)
    return 'data: {}'.format(msg)


def iterator():
    for i in range(CONTENT_SIZE):
        time.sleep(TIME_SLEEP)
        yield gen_message('iteration %06d' % i)


def stream_sync(request):
    """A view that streams a large CSV file."""
    stream = iterator()
    logger.info('Created response')
    response = StreamingHttpResponse(stream, status=200, content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    logger.info('Returned response')
    return response


async def stream_async(request):

    async def event_stream():
        for i in range(CONTENT_SIZE):
            yield gen_message('iteration %06d' % i)
            await asyncio.sleep(TIME_SLEEP)

    return SSE(event_stream(), content_type='text/event-stream')
