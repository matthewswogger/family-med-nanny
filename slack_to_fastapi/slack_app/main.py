import os
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler


slack_app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
SLACK_HANDLER = SlackRequestHandler(slack_app)
    # SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()

@slack_app.event("app_mention")
def handle_app_mention(say, payload):
    user_id = payload["user"]
    say(f"Hey there <@{user_id}>! You mentioned me.")

@slack_app.command("/mycommand")
def handle_my_command(ack, respond, command):
    ack()  # Acknowledge the command
    respond(f"You used the command: {command['text']}")


################################################################

# import os
# from slack_bolt.async_app import (
#     AsyncAck,
#     AsyncApp,
#     # AsyncAssistant,
#     # AsyncBoltContext,
#     # AsyncBoltRequest,
#     # AsyncCustomListenerMatcher,
#     # AsyncGetThreadContext,
#     # AsyncListener,
#     AsyncRespond,
#     # AsyncSaveThreadContext,
#     AsyncSay,
#     # AsyncSetStatus,
#     # AsyncSetSuggestedPrompts,
#     # AsyncSetTitle,
# )
# from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

# slack_app = AsyncApp(token=os.environ.get("SLACK_BOT_TOKEN"))
# SLACK_HANDLER = AsyncSlackRequestHandler(slack_app)


# @slack_app.event("app_mention")
# async def handle_app_mention(say: AsyncSay, payload):
#     user_id = payload["user"]
#     await say(f"Hey there <@{user_id}>! You mentioned me.")

# @slack_app.command("/mycommand")
# async def handle_my_command(ack: AsyncAck, respond: AsyncRespond, command):
#     await ack()  # Acknowledge the command
#     await respond(f"You used the command: {command['text']}")
