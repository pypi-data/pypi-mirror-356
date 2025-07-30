import abc
from pathlib import Path

from pydantic import BaseModel


class FileUploadRequest(BaseModel):
    path: str
    bytes: bytes


class FileUploadResponse(BaseModel):
    uri: str


class FileStore(abc.ABC):
    @abc.abstractmethod
    async def upload(self, request: FileUploadRequest) -> FileUploadResponse:
        pass


class LocalFileStore(FileStore):
    def __init__(self, base_uri: str, directory: str) -> None:
        self.base_uri = base_uri
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    # TODO(@ryunosuke): fix path traversal vulnerability
    async def upload(self, request: FileUploadRequest) -> FileUploadResponse:
        # Save file to public/files directory
        file_path = self.directory / request.path
        with Path.open(file_path, "wb") as f:
            f.write(request.bytes)

        # Return URL for accessing the file
        return FileUploadResponse(uri=f"{self.base_uri}/{request.path}")
