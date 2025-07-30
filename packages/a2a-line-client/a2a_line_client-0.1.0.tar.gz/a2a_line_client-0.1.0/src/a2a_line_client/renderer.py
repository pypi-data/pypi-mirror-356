import abc
import base64
import json
from uuid import uuid4

import a2a.types as a2a
import linebot.v3.messaging as line  # type: ignore[reportMissingImports]

from .file import FileStore, FileUploadRequest  # type: ignore[reportMissingImports]


class A2AToLineMessageRenderer(abc.ABC):
    @abc.abstractmethod
    async def render(self, update: a2a.SendStreamingMessageResponse) -> list[line.Message]:
        pass


class DefaultA2AToLineMessageRenderer(A2AToLineMessageRenderer):
    def __init__(self, file_store: FileStore) -> None:
        self.file_store = file_store

    async def render(self, update: a2a.SendStreamingMessageResponse) -> list[line.Message]:
        if isinstance(update.root, a2a.JSONRPCErrorResponse):
            raise Exception(update.root.error.message or "Unknown error")

        result = update.root.result
        messages: list[line.Message] = []
        if result.kind == "message":
            for part in result.parts:
                messages.append(await self._part_to_line_message(part))
        if result.kind == "artifact-update":
            for part in result.artifact.parts:
                messages.append(await self._part_to_line_message(part))
        if result.kind == "status-update":
            pass
        if result.kind == "task":
            pass

        return messages

    async def _part_to_line_message(self, part: a2a.Part) -> line.Message:
        quick_reply = line.QuickReply(
            items=[
                line.QuickReplyItem(
                    type="action",
                    action=line.PostbackAction(
                        data='{"action": "complete_task"}',
                        displayText="タスクを完了",
                        label="タスクを完了",
                        inputOption=None,
                        fillInText=None,
                    ),
                    imageUrl=None,
                ),
            ],
        )

        if part.root.kind == "file":
            file = part.root.file

            mime_type = file.mimeType
            if not mime_type:
                raise ValueError("mimeType is not set")

            file_type = mime_type.split("/")[0]
            file_extension = mime_type.split("/")[1]

            file_name = uuid4().hex
            file_name = f"{file_name}.{file_extension}"

            file_uri = None
            if isinstance(file, a2a.FileWithBytes):
                file_upload_response = await self.file_store.upload(
                    FileUploadRequest(path=file_name, bytes=base64.b64decode(file.bytes)),
                )
                file_uri = file_upload_response.uri
            else:  # FileWithUrl
                file_uri = file.uri

            if file_type == "image":
                return line.ImageMessage(originalContentUrl=file_uri, previewImageUrl=file_uri, quickReply=quick_reply)
            # TODO(@ryunosuke): support other file types
            return line.TextMessage(text=f"ファイルを送信しました。\n{file_uri}", quickReply=quick_reply, quoteToken=None)

        if part.root.kind == "data":
            return line.TextMessage(text=json.dumps(part.root.data, indent=2), quickReply=quick_reply, quoteToken=None)

        # TextPart
        return line.TextMessage(text=part.root.text, quickReply=quick_reply, quoteToken=None)
