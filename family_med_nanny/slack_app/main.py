import os
import logging
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler
import re

from .utils import SlackHandler


logger = logging.getLogger(__name__)


slack_bot_token = os.environ.get('SLACK_BOT_TOKEN')
slack_signing_secret = os.environ.get('SLACK_SIGNING_SECRET')

app = AsyncApp(
    name='the_slack_app',
    logger=logger,
    token=slack_bot_token,
    signing_secret=slack_signing_secret,
)
SLACK_HANDLER = AsyncSlackRequestHandler(app)


handle_slack = SlackHandler()

re_pattern = re.compile(r"[\s\S]*")


@app.event(re_pattern)
@app.command(re_pattern)
async def handle_everything(args):
    # args.logger.info(
    #     f'\n{"*"*20}\n'
    #     f' Command: {args.command if args.command is not None else False}\n'
    #     f' Message: {args.message if args.message is not None else False}\n'
    #     f'   Event: {args.event if args.event is not None else False}\n'
    #     f' Options: {args.options if args.options is not None else False}\n'
    #     f'Shortcut: {args.shortcut if args.shortcut is not None else False}\n'
    #     f'  Action: {args.action if args.action is not None else False}\n'
    #     f'    View: {args.view if args.view is not None else False}\n'
    #     f'{"*"*20}'
    # )

    if args.command: # args.command.get('command') == '/hey'
        await handle_slack.handle_commands(args)

    elif args.message: # all standard messages
        await handle_slack.handle_messages(args)

    elif args.event:
        if args.event.get('type') == 'team_join':
            await handle_slack.handle_team_join(args)
        else: # args.event.get('type') == 'reaction_added' OR 'file_shared'
            await handle_slack.handle_events(args)

    else: # what didn't I cover?
        args.logger.info(
            f'\n{"*"*20}\n'
            'THIS IS SOMETHING I HAVE NOT COVERED YET\n'
            f' Command: {args.command if args.command is not None else False}\n'
            f' Message: {args.message if args.message is not None else False}\n'
            f'   Event: {args.event if args.event is not None else False}\n'
            f' Options: {args.options if args.options is not None else False}\n'
            f'Shortcut: {args.shortcut if args.shortcut is not None else False}\n'
            f'  Action: {args.action if args.action is not None else False}\n'
            f'    View: {args.view if args.view is not None else False}\n'
            f'{"*"*20}'
        )


@app.error
async def custom_error_handler(error, body, logger):
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
