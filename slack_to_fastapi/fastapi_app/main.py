from fastapi import FastAPI, Request
from urllib.parse import parse_qsl
import json
import logging

# from slack_app.main import SLACK_HANDLER
from slack_app import SLACK_HANDLER


# def parse_req_body(bytes_data):
#     decoded = bytes_data.decode('utf-8').strip()

#     if decoded.startswith('{') or decoded.startswith('['):
#         return json.loads(decoded)

#     return {k: v for k, v in parse_qsl(decoded)}



app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.post('/slack/events')
async def slack_events(req: Request):
    # bod = await req.body()
    # parsed_bod = parse_req_body(bod)

    # print(f'\n\nreq:\n {parsed_bod}\n\n', flush=True)

    return await SLACK_HANDLER.handle(req)
