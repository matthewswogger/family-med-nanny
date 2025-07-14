import os
import logging
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
import re

from med_nannyai import MedNannyAI


med_nannyai = MedNannyAI()


# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

# https://tools.slack.dev/bolt-python/api-docs/slack_bolt/
# https://tools.slack.dev/python-slack-sdk/api-docs/slack_sdk/

app = App(
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET')
)
SLACK_HANDLER = SlackRequestHandler(app)


def block_buster(event: dict):
    block = event.get('blocks', {})[0]
    block_elements = block.get('elements', {})[0].get('elements', {})
    return block_elements



def parse_slack_mentions(text: str) -> dict[str, list[str | None]]:
    # matches this: <@USER_ID> or <@USER_ID|display_name>
    user_matches = set(re.findall(r'<@([A-Z0-9]+)(?:\|[^>]*)?>', text))

    # matches this: <#CHANNEL_ID> or <#CHANNEL_ID|channel_name>
    channel_matches = set(re.findall(r'<#([A-Z0-9]+)(?:\|[^>]*)?>', text))

    return {
        'referred_to_user_id': list(user_matches) or [],
        'referred_to_channel_id': list(channel_matches) or []
    }



@app.command('/hey')
def handle_hey_command(ack, command, client, context, logger):
    # acknowledge using mysterious slack magic
    ack()
    # ack(f"Hi <@{command['user_id']}>!")


    # 1) get the things you need from `command`, `context`
    user_text = command.get('text')
    channel_id = command.get('channel_id')


    # 2) use `MedNannyAI` to craft what will be said to the user etc



    # 3) send whatever message you need to to the user
    response = client.chat_postMessage(
        channel=channel_id,
        text=f'Here is what I got for you: {user_text}',
    )
    logger.info(f'\n\n/hey:\n {command}\n\n')



@app.event('message')
def handle_message_events(event, client, context, logger):

    # 1) get the things you need from `event`, `context`
    channel_id = event.get('channel')
    user_text = event.get('text')

    block = event.get('blocks')[0]
    block_elements = block.get('elements')[0].get('elements')


    # 2) use `MedNannyAI` to craft what will be said to the user etc



    # 3) send whatever message you need to to the user
    response = client.chat_postMessage(
        channel=channel_id,
        text=f'Here is what I got for you: {user_text}',
    )
    # response = client.chat_postEphemeral(
    #     channel=channel_id,
    #     user=user_id,
    #     text=f'Here is what I got for you: {user_text}',
    # )
    logger.info(f'\n\nmessage:\n {event}\n\n')




# client.chat_postMessage : Sends a message to a channel.
    # client.chat_postEphemeral : Sends an ephemeral message to a user in a channel.
# client.chat_scheduleMessage : Schedules a message.
# client.chat_scheduledMessages_list : Lists all scheduled messages.
# client.chat_deleteScheduledMessage : Deletes a scheduled message.

# client.conversations_replies : Retrieve a thread of messages posted to a conversation
# client.conversations_history : Fetches a conversation's history of messages and events.
# client.conversations_info : Retrieves information about a conversation.
# client.conversations_list : Lists all channels in a Slack team.
# client.conversations_members : Lists members of a conversation.

# client.users_list : Lists all users in a Slack team.
# client.users_identity : Get a user's identity.
# client.users_profile_get : Retrieves a user's profile information.

# client.reactions_add : Adds a reaction to an item.

# client.channels_history : Fetches history of messages and events from a channel.
# client.channels_list : Lists all channels in a Slack team.
# client.channels_replies : Retrieve a thread of messages posted to a channel.

# client.emoji_list : Lists custom emoji for a team.

# client.search_messages : Searches for messages matching a query.


