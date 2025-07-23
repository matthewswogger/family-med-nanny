import os
import logging
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_sdk import WebClient
import re
from typing import Any, Literal

from .utils import SlackHandler
from med_nannyai import Slack_MedNannyAI


# class LogTemplate(str):
#     DEFAULT_TEMPLATE = '{levelname} - {asctime} - {name} - {message}'
#     FORMAT_TEMPLATE = '{levelname:<10}Timestamp: {asctime} : {name} : {message}'

#     def __new__(cls, template=None):
#         if template is None:
#             template = cls.DEFAULT_TEMPLATE
#         return super().__new__(cls, template)

#     def __init__(self, template=None):
#         self.template = template or self.DEFAULT_TEMPLATE
#         super().__init__()

#     def format(self, **kwargs):
#         kwargs['asctime'] = kwargs['asctime'].replace(',', '.')
#         kwargs['levelname'] = f"{kwargs['levelname']}:"

#         return self.FORMAT_TEMPLATE.format(**kwargs)

#     def __repr__(self):
#         return f'{super().__repr__()}'


logger = logging.getLogger(__name__)

# logging.basicConfig(
#     level=logging.INFO,
#     format=LogTemplate(),
#     style="{"
# )

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
    args.logger.info(
        f'\n{"*"*20}\n'
        f' Command present: {args.command is not None}\n'
        f' Message present: {args.message is not None}\n'
        f'   Event present: {args.event is not None}\n'
        f' Options present: {args.options is not None}\n'
        f'Shortcut present: {args.shortcut is not None}\n'
        f'  Action present: {args.action is not None}\n'
        f'    View present: {args.view is not None}\n'
        f'{"*"*20}'
    )

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






# @app.event('file_shared')
# def handle_file_shared_events(event, say, client, context, body, logger):
#     logger.info(f'\n\n{"-"*100}\n\n{body}\n\n{"-"*100}\n\n')
#     logger.info(f'\n\n{"-"*100}\n\n{event}\n\n{"-"*100}\n\n')
    
#     # Get file information from the event
#     file_info = event.get('file', {})
#     file_id = file_info.get('id')
    
#     if file_id:
#         try:
#             # Get detailed file info using slack_sdk
#             file_details = client.files_info(file=file_id)
#             logger.info(f"File details: {file_details}")
            
#             # Get the file content/URL
#             file_url = file_details['file']['url_private']
#             file_name = file_details['file']['name']
#             file_type = file_details['file']['mimetype']
            
#             logger.info(f"File URL: {file_url}")
#             logger.info(f"File name: {file_name}")
#             logger.info(f"File type: {file_type}")
            
#             # Download the file content if needed
#             headers = {'Authorization': f'Bearer {os.environ.get("SLACK_BOT_TOKEN")}'}
#             response = requests.get(file_url, headers=headers)
            
#             if response.status_code == 200:
#                 file_content = response.content
#                 logger.info(f"Successfully downloaded file: {file_name} ({len(file_content)} bytes)")
                
#                 # Save file locally if needed
#                 # with open(f"downloads/{file_name}", "wb") as f:
#                 #     f.write(file_content)
                
#                 # Process the file content here
#                 # For example, if it's an image, you could process it
#                 if file_type.startswith('image/'):
#                     logger.info("Processing image file...")
#                     # Add your image processing logic here
#                 elif file_type == 'application/pdf':
#                     logger.info("Processing PDF file...")
#                     # Add your PDF processing logic here
#                 else:
#                     logger.info(f"Processing {file_type} file...")
#                     # Add your file processing logic here
#             else:
#                 logger.error(f"Failed to download file: {response.status_code}")
            
#         except Exception as e:
#             logger.error(f"Error getting file info: {e}")
#     else:
#         logger.warning("No file ID found in event")













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
