import asyncio
import nest_asyncio

from django.http.response import StreamingHttpResponse


class SSEResponse(StreamingHttpResponse):

    def __init__(self, streaming_content=(), *args, **kwargs):
        sync_streaming_content = self.get_sync_iterator(streaming_content)
        super().__init__(streaming_content=sync_streaming_content, *args, **kwargs)

    @staticmethod
    async def convert_async_iterable(stream):
        """Accepts async_generator and async_iterator"""
        return iter([chunk async for chunk in stream])

    def get_sync_iterator(self, async_iterable):
        nest_asyncio.apply()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.convert_async_iterable(async_iterable))
        return result
