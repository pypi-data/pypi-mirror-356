import os

import uvicorn
from dotenv import load_dotenv

from a2a_line_client import (
    DefaultA2AToLineMessageRenderer,
    DefaultLineEventHandler,
    DefaultLineToA2AMessageParser,
    InMemoryUserStateStore,
    LocalFileStore,
    Worker,
    build_server,
)

if __name__ == "__main__":
    load_dotenv()

    user_state_store = InMemoryUserStateStore()
    parser = DefaultLineToA2AMessageParser()
    renderer = DefaultA2AToLineMessageRenderer(file_store=LocalFileStore(base_uri=f"{os.getenv('HOST') or ''}/files", directory="public/files"))
    handler = DefaultLineEventHandler(os.getenv("LINE_CHANNEL_ACCESS_TOKEN") or "", os.getenv("A2A_AGENT_CARD_URL") or "", user_state_store, parser, renderer)
    worker = Worker(os.getenv("LINE_CHANNEL_SECRET") or "", handler)

    server = build_server(worker)

    uvicorn.run(server, host="0.0.0.0", port=8000)
