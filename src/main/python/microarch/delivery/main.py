# microarch/delivery/main.py
import asyncio

import uvicorn
from fastapi import FastAPI


def create_app() -> FastAPI:
    return FastAPI(title="Delivery Service", version="1.0.0")


async def main() -> None:
    app = create_app()

    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
