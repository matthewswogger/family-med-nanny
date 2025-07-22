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
    s = '*'*100
    # logger.info(f'\n{s}\n{req}\n{s}\n')
    sh = await SLACK_HANDLER.handle(req)
    # logger.info(f'\n{s}\n{sh}\n{s}\n')
    return sh
