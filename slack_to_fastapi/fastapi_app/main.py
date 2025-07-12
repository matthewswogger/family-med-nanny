from fastapi import FastAPI, Request
from slack_app.main import SLACK_HANDLER


api = FastAPI()

@api.get("/")
async def root():
    return {"message": "Hello World"}


@api.post("/slack/events")
async def slack_events(req: Request):
    return await SLACK_HANDLER.handle(req)
