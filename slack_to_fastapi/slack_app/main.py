import os
import logging
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_sdk import WebClient
import re
from typing import Any, Literal

from .utils import GetSlackUserAndChannelInfo, EnrichUserIDs, EnrichChannelIDs
from med_nannyai import Slack_MedNannyAI


class LogTemplate(str):
    DEFAULT_TEMPLATE = '{levelname} - {asctime} - {name} - {message}'
    FORMAT_TEMPLATE = '{levelname:<10}Timestamp: {asctime} : {name} : {message}'

    def __new__(cls, template=None):
        if template is None:
            template = cls.DEFAULT_TEMPLATE
        return super().__new__(cls, template)

    def __init__(self, template=None):
        self.template = template or self.DEFAULT_TEMPLATE
        super().__init__()

    def format(self, **kwargs):
        kwargs['asctime'] = kwargs['asctime'].replace(',', '.')
        kwargs['levelname'] = f"{kwargs['levelname']}:"

        return self.FORMAT_TEMPLATE.format(**kwargs)

    def __repr__(self):
        return f'{super().__repr__()}'


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format=LogTemplate(),
    style="{"
)


# https://tools.slack.dev/bolt-python/api-docs/slack_bolt/
# https://tools.slack.dev/python-slack-sdk/api-docs/slack_sdk/
# https://api.slack.com/methods

app = App(
    name='slack_MedNannyAI',
    logger=logger,
    token=os.environ.get('SLACK_BOT_TOKEN'),
    signing_secret=os.environ.get('SLACK_SIGNING_SECRET'),
)
SLACK_HANDLER = SlackRequestHandler(app)


client = WebClient(token=os.environ.get('SLACK_BOT_TOKEN'))
# users_info, channels_info = GetSlackUserAndChannelInfo()(client)


######################################################################################
# Slack Events, Commands, etc
######################################################################################

@app.event("team_join")
def ask_for_introduction(event, say, client, context, logger):
    welcome_channel_id = "C12345"
    user_id = event["user"]
    text = f"Welcome to the team, <@{user_id}>! :tada: You can introduce yourself in this channel."
    say(text=text, channel=welcome_channel_id)


@app.command('/hey')
def handle_hey_command(ack, command, client, context, logger):
    # acknowledge using mysterious slack magic
    ack()
    # ack(f"Hi <@{command['user_id']}>!")

    # 1) get the things you need from `command`, `context`
    user_text = command.get('text')
    # user_mentions, channel_mentions = parse_slack_mentions(user_text)
    channel_id = command.get('channel_id')

    # 2) use `MedNannyAI` to craft what will be said to the user etc


    # 3) send whatever message you need to to the user
    response = client.chat_postMessage(
        channel=channel_id,
        text=f'Here is what I got for you: {user_text}',
    )
    logger.info(f'{command}\n\n')



@app.event('message')
def handle_message_events(event, client, context, logger):
    # 1) get the things you need from `event`, `context`


    # enriched_user_ids = EnrichUserIDs(users_info, request_type='message')
    # enriched_channel_ids = EnrichChannelIDs(channels_info, request_type='message')


    user_text = event.get('text')
    channel_id = event.get('channel')
    user_id = event.get('user')
    event_ts = event.get('event_ts') or event.get('ts')


    # user_name_map = lambda x: f'<@{x}>'
    # channel_name_map = lambda x: f'<#{x}|>'

    # slack_user_names_map = {
    #     user_name_map('U0957BCUP7S'): 'Matthew May',
    # }
    # slack_channel_names_map = {
    #     channel_name_map('C0957BD4UFJ'): '#social',
    #     channel_name_map('C0957BD49H6'): '#all-day-of-may'
    # }
    # llm_user_text = replace_multiple_substrings(user_text, slack_user_names_map)
    # llm_user_text = replace_multiple_substrings(llm_user_text, slack_channel_names_map)

    # 2) use `MedNannyAI` to craft what will be said to the user etc
    # med_nanny_response = Slack_MedNannyAI.process_user_input(
    #     user_message=llm_user_text,
    #     user_name='Matthew May',
    #     user_id=123
    # )

    # 3) send whatever message you need to to the user
    response = client.chat_postMessage(
        channel=channel_id,
        # text=med_nanny_response
        text=f'Here is what I got for you: {user_text}',
    )
    # response = client.chat_postEphemeral(
    #     channel=channel_id,
    #     user=user_id,
    #     text=med_nanny_response
    # )
    logger.info(f'{event}\n\n')


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
