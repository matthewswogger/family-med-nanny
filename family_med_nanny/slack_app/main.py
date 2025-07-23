import os
import logging
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_sdk import WebClient
import re
# from typing import Any, Literal

from .utils import SlackHandler
# from med_nannyai import Slack_MedNannyAI


logger = logging.getLogger(__name__)


slack_bot_token = os.environ.get('SLACK_BOT_TOKEN')
slack_signing_secret = os.environ.get('SLACK_SIGNING_SECRET')

app = App(
    name='the_slack_app',
    logger=logger,
    token=slack_bot_token,
    signing_secret=slack_signing_secret,
)
SLACK_HANDLER = SlackRequestHandler(app)


handle_slack = SlackHandler(
    client=WebClient(token=slack_bot_token)
)

re_pattern = re.compile(r"[\s\S]*")

# @app.event("team_join")
# def ask_for_introduction(event, say, client, context, logger):
#     welcome_channel_id = "C12345"
#     user_id = event["user"]
#     text = f"Welcome to the team, <@{user_id}>! :tada: Introduce yourself."
#     say(text=text, channel=welcome_channel_id)


@app.event(re_pattern)
@app.command(re_pattern)
def handle_everything(args):
    # args.logger.info(
    #     f'\n{"*"*20}\n'
    #     f' Command present: {args.command is not None}\n'
    #     f' Message present: {args.message is not None}\n'
    #     f'   Event present: {args.event is not None}\n'
    #     f' Options present: {args.options is not None}\n'
    #     f'Shortcut present: {args.shortcut is not None}\n'
    #     f'  Action present: {args.action is not None}\n'
    #     f'    View present: {args.view is not None}\n'
    #     f'{"*"*20}'
    # )

    if args.command: # args.command.get('command') == '/hey'
        handle_slack.handle_commands(args)

    elif args.message: # all standard messages
        handle_slack.handle_messages(args)

    elif args.event: # args.event.get('type') == 'reaction_added' OR 'file_shared'
        handle_slack.handle_events(args)

    else: # what didn't I cover?
        args.logger.info(
            f'\n{"*"*20}\n'
            'THIS IS SOMETHING I HAVEN\'T COVERED YET\n'
            f' Command: {args.command}\n'
            f' Message: {args.message}\n'
            f'   Event: {args.event}\n'
            f' Options: {args.options}\n'
            f'Shortcut: {args.shortcut}\n'
            f'  Action: {args.action}\n'
            f'    View: {args.view}\n'
            f'{"*"*20}'
        )



@app.error
def custom_error_handler(error, body, logger):
    logger.exception(f'Error: {error}')
    logger.info(f'Request body: {body}')



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
