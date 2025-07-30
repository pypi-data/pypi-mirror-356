import abc
import json
import logging
from collections.abc import AsyncGenerator
from uuid import uuid4

import httpx
from a2a.client import A2AClient
from a2a.types import JSONRPCErrorResponse, MessageSendParams, SendStreamingMessageRequest, SendStreamingMessageResponse, Task
from linebot.v3.messaging import (  # type: ignore[reportMissingImports]
    Configuration,  # type: ignore[reportMissingImports]
    Message,
    TextMessage,
)
from linebot.v3.webhooks import Event, MessageEvent, PostbackEvent, UserSource  # type: ignore[reportMissingImports]

from .parser import LineToA2AMessageParser
from .renderer import A2AToLineMessageRenderer
from .sender import ReplyAndPushLineMessageSender
from .user_state import UserState, UserStateStore


class LineEventHandler(abc.ABC):
    @abc.abstractmethod
    async def handle(self, event: Event) -> None:
        pass


logger = logging.getLogger(__name__)


class DefaultLineEventHandler(LineEventHandler):
    def __init__(
        self,
        channel_access_token: str,
        a2a_agent_card_url: str,
        user_state_store: UserStateStore,
        parser: LineToA2AMessageParser,
        renderer: A2AToLineMessageRenderer,
    ) -> None:
        self.configuration = Configuration(access_token=channel_access_token)
        self.a2a_agent_card_url = a2a_agent_card_url
        self.user_state_store = user_state_store
        self.parser = parser
        self.renderer = renderer

    async def handle(self, event: Event) -> None:
        if isinstance(event, MessageEvent):
            await self._handle_message(event)
        elif isinstance(event, PostbackEvent):
            await self._handle_postback(event)
        else:
            # TODO(@ryunosuke): handle other events
            raise ValueError(f"unsupported event: {event.type}")

    async def _handle_message(self, event: MessageEvent) -> None:
        if not event.source or not isinstance(event.source, UserSource):
            raise ValueError("only single user conversation is supported")

        line_user_id = event.source.user_id or ""

        self.sender = ReplyAndPushLineMessageSender(
            reply_token=event.reply_token or "",
            target_user_id=line_user_id,
            configuration=self.configuration,
            reply_message_count=3,
        )

        reply_token = event.reply_token
        if reply_token is None:
            raise ValueError("reply_token is not set")

        await self.sender.run(self._generate_messages(line_user_id, event))

    async def _handle_postback(self, event: PostbackEvent) -> None:
        if not event.source or not isinstance(event.source, UserSource):
            raise ValueError("only single user conversation is supported")

        line_user_id = event.source.user_id or ""
        postback_data = event.postback.data

        sender = ReplyAndPushLineMessageSender(
            reply_token=event.reply_token or "",
            target_user_id=line_user_id,
            configuration=self.configuration,
            reply_message_count=5,
        )

        async def send_message(messages: list[Message]) -> None:
            async def generate_message():
                for message in messages:
                    yield message

            await sender.run(generate_message())

        try:
            data = json.loads(postback_data)

            if data.get("action") == "complete_task":
                # user_stateを初期化
                await self.user_state_store.set(line_user_id, UserState(task_id=None, context_id=None))
                await send_message([TextMessage(text="タスクを完了しました。新しいタスクを開始できます。", quickReply=None, quoteToken=None)])
            else:
                await send_message([TextMessage(text="不明なアクションです。", quickReply=None, quoteToken=None)])

        except json.JSONDecodeError:
            await send_message([TextMessage(text="不明なアクションです。", quickReply=None, quoteToken=None)])

    async def _generate_messages(self, user_id: str, event: MessageEvent) -> AsyncGenerator[Message]:
        user_state = await self.user_state_store.get(user_id)
        print(user_state)

        user_message = self.parser.parse(event.message)
        if user_state.task_id:
            user_message.taskId = user_state.task_id
        if user_state.context_id:
            user_message.contextId = user_state.context_id

        try:
            async with httpx.AsyncClient() as httpx_client:
                client = await A2AClient.get_client_from_agent_card_url(
                    httpx_client,
                    self.a2a_agent_card_url,
                )

                streaming_request = SendStreamingMessageRequest(
                    id=uuid4().hex,
                    params=MessageSendParams(
                        message=user_message,
                    ),
                )
                stream_response = client.send_message_streaming(streaming_request)
                async for update in stream_response:
                    for message in await self.renderer.render(update):
                        yield message

                    task_id = _get_task_id(update)
                    context_id = _get_context_id(update)
                    await self.user_state_store.set(user_id, UserState(task_id=task_id, context_id=context_id))

        except Exception:
            logger.exception("error occurred while sending message to A2A")
            yield TextMessage(text="エラーが発生しました。", quickReply=None, quoteToken=None)


def _get_task_id(update: SendStreamingMessageResponse) -> str | None:
    if isinstance(update.root, JSONRPCErrorResponse):
        return None
    if isinstance(update.root.result, Task):
        return update.root.result.id
    return update.root.result.taskId


def _get_context_id(update: SendStreamingMessageResponse) -> str | None:
    if isinstance(update.root, JSONRPCErrorResponse):
        return None
    return update.root.result.contextId
