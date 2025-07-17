from dotenv import load_dotenv

load_dotenv()

import logfire
from contextlib import asynccontextmanager
from fastapi import FastAPI

from routes import routes_app, routes_frontend
from conversation_storage import Database
from utils import THIS_DIR


# 'if-token-present' means nothing will
# be sent (and the example will work) if
# you don't have logfire configured
logfire.configure(send_to_logfire='if-token-present')
logfire.instrument_pydantic_ai()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield {'db': Database()}


app = FastAPI(lifespan=lifespan)
logfire.instrument_fastapi(app)

app.include_router(routes_frontend.router)
app.include_router(routes_app.router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        reload=True,
        reload_dirs=[str(THIS_DIR)]
    )
