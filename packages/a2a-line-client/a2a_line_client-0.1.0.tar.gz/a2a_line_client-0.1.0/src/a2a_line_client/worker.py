import asyncio
from concurrent.futures import ThreadPoolExecutor

from linebot.v3 import WebhookParser  # type: ignore[reportMissingImports]
from linebot.v3.webhooks import Event  # type: ignore[reportMissingImports]

from .handler import LineEventHandler  # type: ignore[reportMissingImports]


class Worker:
    def __init__(self, channel_secret: str, handler: LineEventHandler) -> None:
        self.executor = ThreadPoolExecutor(thread_name_prefix="line_events")
        self.parser = WebhookParser(channel_secret)
        self.handler = handler

    def submit(self, data: str, signature: str) -> None:
        self.executor.submit(self._process_events, data, signature)

    def _process_events(self, data: str, signature: str) -> None:
        events: list[Event] = self.parser.parse(data, signature)  # type: ignore[reportUnknownReturnType]
        for event in events:
            asyncio.run(self.handler.handle(event))
