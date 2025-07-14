import os
import logging
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler


# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

app = App(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)
SLACK_HANDLER = SlackRequestHandler(app)

@app.command('/hey')
def handle_hey_command(ack, say, command, logger):

    # ack() # do slack magic
    ack(f"Hi <@{command['user_id']}>!") # do slack magic

    channel_id = command.get('channel_id')
    user_text = command.get('text')
    response_url = command.get('response_url')

    say(f'Here is what I got for you: {user_text}')

    # logger.info(f'\n\n/hey:\n {command}\n\n')

@app.event('message')
def handle_message_events(event, client, logger):

    channel_type = event.get('channel_type')
    channel_id = event.get('channel')
    user_id = event.get('user')
    user_text = event.get('text')
    utc_epoch = event.get('event_ts')

    response = client.chat_postMessage(
        channel=channel_id,
        text=f'Hello from your app! :tada: you said: {user_text} and you are {user_id} in {channel_id}',
    )
    # response = client.chat_postEphemeral(
    #     channel=channel_id,
    #     user=user_id,
    #     text=f'Hello from your app! :tada: you said: {user_text} and you are {user_id} in {channel_id}',
    # )
    # logger.info(f'\n\nmessage:\n {event}\n\n')


################################################################
################################################################
################################################################
################################################################


# import os
# from slack_bolt import App
# from slack_bolt.adapter.fastapi import SlackRequestHandler


# slack_app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
# SLACK_HANDLER = SlackRequestHandler(slack_app)
#     # SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN")).start()

# @slack_app.event("app_mention")
# def handle_app_mention(say, payload):
#     user_id = payload["user"]
#     say(f"Hey there <@{user_id}>! You mentioned me.")

# @slack_app.command("/mycommand")
# def handle_my_command(ack, respond, command):
#     ack()  # Acknowledge the command
#     respond(f"You used the command: {command['text']}")


################################################################
################################################################
################################################################
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
