import abc
from collections.abc import AsyncGenerator

import linebot.v3.messaging as line  # type: ignore[reportMissingImports]
from linebot.v3.messaging import (  # type: ignore[reportMissingImports]
    ApiClient,
    Configuration,
    MessagingApi,
    PushMessageRequest,
    ReplyMessageRequest,
    ShowLoadingAnimationRequest,
)


class LineMessageSender(abc.ABC):
    @abc.abstractmethod
    async def run(self, message_generator: AsyncGenerator[line.Message]) -> None:
        pass


MAX_REPLY_MESSAGE_COUNT = 5


class ReplyAndPushLineMessageSender(LineMessageSender):
    def __init__(self, reply_token: str, target_user_id: str, configuration: Configuration, reply_message_count: int = 3) -> None:
        self.reply_token = reply_token
        self.target_user_id = target_user_id
        self.configuration = configuration

        if reply_message_count > MAX_REPLY_MESSAGE_COUNT:
            raise ValueError("reply_message_count must be less than or equal to 5")
        self.reply_message_count = reply_message_count

    async def run(self, message_generator: AsyncGenerator[line.Message]) -> None:
        await self._show_loading_animation()

        reply_messages: list[line.Message] = []
        async for message in message_generator:
            if len(reply_messages) < self.reply_message_count:
                reply_messages.append(message)
                if len(reply_messages) == self.reply_message_count:
                    await self._send_reply_message(reply_messages)
            else:
                await self._send_push_message(message)

        if len(reply_messages) < self.reply_message_count:
            await self._send_reply_message(reply_messages)

    async def _show_loading_animation(self) -> None:
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.show_loading_animation_with_http_info(  # type: ignore[reportUnknownReturnType]
                ShowLoadingAnimationRequest(
                    chatId=self.target_user_id,
                    loadingSeconds=60,
                ),
            )

    async def _send_reply_message(self, messages: list[line.Message]) -> None:
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(  # type: ignore[reportUnknownReturnType]
                ReplyMessageRequest(
                    replyToken=self.reply_token,
                    messages=messages,
                    notificationDisabled=False,
                ),
            )

    async def _send_push_message(self, message: line.Message) -> None:
        with ApiClient(self.configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.push_message_with_http_info(  # type: ignore[reportUnknownReturnType]
                PushMessageRequest(
                    to=self.target_user_id,
                    messages=[message],
                    notificationDisabled=False,
                    customAggregationUnits=None,
                ),
            )
