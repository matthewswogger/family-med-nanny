import uvicorn
import asyncio
import os
import signal
from uvicorn import Server, Config
from pyngrok import ngrok
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


async def run_fastapi():
    config = Config(
        app='fastapi_app.main:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
        reload_dirs=[str(Path(__file__).parent)]
    )
    server = Server(config)
    await server.serve()


async def run_ngrok():
    # ngrok_tunnel = ngrok.connect(name='fastapi-ngrok-tunnel')
    ngrok_tunnel = ngrok.connect(name='blaw')

    print(f'FastAPI app exposed at: {ngrok_tunnel.public_url}', flush=True)


async def main():
    await asyncio.gather(run_fastapi(), run_ngrok())


if __name__ == '__main__':
    # uvicorn.run(
    #     'fastapi_app.main:app',
    #     host='127.0.0.1',
    #     port=8000,
    #     reload=True,
    #     reload_dirs=[str(Path(__file__).parent)],
    # )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        os.kill(os.getpid(), signal.SIGTERM)
