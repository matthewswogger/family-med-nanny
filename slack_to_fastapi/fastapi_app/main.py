from fastapi import FastAPI, Request
# from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from slack_app import SLACK_HANDLER

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


app = FastAPI()


@app.get('/')
async def root():
    return {'message': 'Hello World'}

@app.post('/slack/events')
async def slack_events(req: Request):
    return await SLACK_HANDLER.handle(req)



##################################################################
# If I need to work with the raw request I'll use the below code.
# Sor far I don't need to and don't see needing it in the future.
##################################################################
# from fastapi import FastAPI, Request
# from urllib.parse import parse_qsl
# import json
# import logging

# from slack_app import SLACK_HANDLER


# def parse_req_body(bytes_data):
#     decoded = bytes_data.decode('utf-8').strip()

#     if decoded.startswith('{') or decoded.startswith('['):
#         return json.loads(decoded)

#     return {k: v for k, v in parse_qsl(decoded)}


# app = FastAPI()

# @app.get('/')
# async def root():
#     return {'message': 'Hello World'}


# @app.post('/slack/events')
# async def slack_events(req: Request):
#     bod = await req.body()
#     parsed_bod = parse_req_body(bod)

#     print(f'\n\nreq:\n {parsed_bod}\n\n', flush=True)

#     return await SLACK_HANDLER.handle(req)
