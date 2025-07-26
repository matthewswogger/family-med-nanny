from fastapi import FastAPI, Request
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from slack_app import SLACK_HANDLER

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post('/slack/events')
async def slack_events(req: Request):
    sh = await SLACK_HANDLER.handle(req)
    return sh
