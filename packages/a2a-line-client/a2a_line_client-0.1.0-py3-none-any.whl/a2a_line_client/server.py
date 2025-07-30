from fastapi import FastAPI, Request, Response
from starlette.staticfiles import StaticFiles

from .worker import Worker


def build_server(worker: Worker) -> FastAPI:
    # ruff: noqa: ANN201
    async def callback(request: Request) -> Response:
        # get X-Line-Signature header value
        signature = request.headers.get("X-Line-Signature", "")

        # get request body as text
        body = await request.body()
        body_str = body.decode()

        worker.submit(body_str, signature)

        return Response(status_code=200)

    app = FastAPI()
    app.post("/callback")(callback)
    app.mount("/files", StaticFiles(directory="public/files"), name="files")
    return app
