import abc

import a2a.types as a2a
import linebot.v3.webhooks as line  # type: ignore[reportMissingImports]


class LineToA2AMessageParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, content: line.MessageContent) -> a2a.Message:
        pass


class DefaultLineToA2AMessageParser(LineToA2AMessageParser):
    def parse(self, content: line.MessageContent) -> a2a.Message:
        if isinstance(content, line.TextMessageContent):
            return a2a.Message(
                role=a2a.Role.user,
                parts=[
                    a2a.Part(a2a.TextPart(text=content.text)),
                ],
                messageId=f"line-message-{content.id}",
            )
        # if isinstance(content, line.FileMessageContent):
        # if isinstance(content, line.ImageMessageContent):
        # if isinstance(content, line.VideoMessageContent):
        # if isinstance(content, line.AudioMessageContent):
        # if isinstance(content, line.LocationMessageContent):
        # if isinstance(content, line.StickerMessageContent):

        raise ValueError(f"unsupported message content: {content.type}")
