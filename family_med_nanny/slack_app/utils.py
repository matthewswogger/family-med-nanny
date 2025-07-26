import httpx
import os
import re
from typing import Any
from logging import Logger
from slack_sdk.web.async_client import AsyncWebClient
from typing import Any, Literal
from cachetools import TTLCache

from med_nannyai import Slack_MedNannyAI
from utils import async_cached


class SlackHandler:
    def __init__(self):
        self.after_pad: str = f'{"*"*20}'
        self.before_pad: str = f'\n{self.after_pad}\n'

    ###################################################################################
    async def handle_commands(self, args):
        args.ack() # ack(f"Hi <@{args.command['user_id']}>!")

        users_info = await self._query_slack_for_user_ids(client=args.client, logger=args.logger)
        channels_info = await self._query_slack_for_channel_ids(client=args.client, logger=args.logger)

        user_id = args.command.get('user_id') # this is who just sent the /slash command
        channel_id = args.command.get('channel_id')
        user_text = args.command.get('text')
        user_mentions = self._parse_slack_mentions(text=user_text, parse_type='users')
        channel_mentions = self._parse_slack_mentions(text=user_text, parse_type='channels')

        response = await args.client.chat_postMessage(
            channel=channel_id,
            text=f'Here is what I got for you: {user_text}',
        )

    ###################################################################################
    async def handle_messages(self, args):

        # Get the easy stuff from the message
        user_id = args.message.get('user') # this is who just sent the message
        channel_id = args.message.get('channel')
        user_text = args.message.get('text')
        message_timestamp = args.message.get('event_ts') or args.message.get('ts')
        file_blocks = args.message.get('files', [])


        # get all the users that exist in the slack workspace
        # get any users that were mentioned in the current message
        # map the slack specific user_id's to the user_name's
        users_info = await self._query_slack_for_user_ids(client=args.client, logger=args.logger)
        user_mentions = self._parse_slack_mentions(text=user_text, parse_type='users')
        user_names_map = self._map_slack_encodings_to_readable_text(users_info, user_mentions+[user_id], 'users')

        # Remove <@ and > from all keys in user_names_map
        parsed_user_names_map = {
            k.replace('<@', '').replace('>', ''): v for k, v in user_names_map.items()
        }

        user_name = parsed_user_names_map[user_id]

        # args.logger.info(
        #     f'{self.before_pad}'
        #     f'parsed_user_names_map:\n{parsed_user_names_map}\n'
        #     f'user_name:\n{user_name}\n'
        #     f'{self.after_pad}'
        # )

        # get all the channels that exist in the slack workspace
        # get any channels that were mentioned in the current message
        # map the slack specific channel_id's to the channel_name's
        channels_info = await self._query_slack_for_channel_ids(client=args.client, logger=args.logger)
        channel_mentions = self._parse_slack_mentions(text=user_text, parse_type='channels')
        channel_names_map = self._map_slack_encodings_to_readable_text(channels_info, channel_mentions+[channel_id], 'channels')

        # replace the slack specific user_id's and channel_id's with the user_name's and channel_name's
            # this is prepping the text for the LLM
        llm_user_text = self._replace_multiple_substrings(user_text, user_names_map)
        llm_user_text = self._replace_multiple_substrings(llm_user_text, channel_names_map)


        # get all files that were posibly uploaded with the current message
        bad_urls, good_files = await self._if_message_has_files_get_files(file_blocks, strict=False)


        med_nanny_response = await Slack_MedNannyAI.process_user_input(
            user_message=llm_user_text,
            user_name=user_name,
            user_id=user_id,
            image_files=good_files,
            family_names_map=parsed_user_names_map
        )

        response = await args.client.chat_postMessage(
            channel=channel_id,
            text=med_nanny_response
        )
        # response = await args.client.chat_postEphemeral(
        #     channel=channel_id,
        #     user=user_id,
        #     text=med_nanny_response
        # )


    async def handle_team_join(self, args):

        welcome_channel_id = 'C12345' # TODO: this is fake for now
        user_id = args.event['user']

        response = await args.client.chat_postMessage(
            channel=welcome_channel_id,
            text=f'Welcome to the team, <@{user_id}>! :tada: Introduce yourself.'
        )


    ###################################################################################
    async def handle_events(self, args):

        if args.event.get('type') in ['reaction_added']:
            users_info = await self._query_slack_for_user_ids(client=args.client, logger=args.logger)
            channels_info = await self._query_slack_for_channel_ids(client=args.client, logger=args.logger)

            channel_id = args.event.get('item').get('channel')
            user_reaction = args.event.get('reaction')

            response = await args.client.chat_postMessage(
                channel=channel_id,
                # text=med_nanny_response
                text=f'Here is what I got for you: {user_reaction}',
            )
            # response = args.client.chat_postEphemeral(
            #     channel=channel_id,
            #     user=user_id,
            #     text=med_nanny_response
            # )


    async def _if_message_has_files_get_files(self, file_blocks: list, strict: bool=False) -> tuple[list[str | None], list[tuple[str, str, Any] | None]]:
        '''
        If a message has a 'files' block in it:
            - We look for 'mimetype' of 'image/*' so we can get the urls for them.
            - This allows the bot to know that someone uploaded a pic of a prescription bottle
              and it might need to OCR that bad boy.
            - If strict is False, we will return all the urls, not just the image urls.

        Then we fetch the files from Slack:
            - If the file is queried for successfully, we add it to the good_files list.
            - If something goes wrong, we add the url to the bad_urls list.
        '''
        urls = []

        if strict:
            urls = [file.get('url_private') for file in file_blocks if file.get('mimetype', '').startswith('image/')]
        else:
            urls = [file.get('url_private') for file in file_blocks if file.get('mimetype')]

        if not urls:
            return [], []

        SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
        headers = {'Authorization': f'Bearer {SLACK_BOT_TOKEN}'}

        bad_urls: list[str | None] = []
        good_files: list[tuple[str, str, Any] | None] = []

        async with httpx.AsyncClient() as client:
            for url in urls:
                response = await client.get(url=url, headers=headers)
                if response.is_success:
                    good_files.append((url, response.headers['content-type'], response.content))
                else:  # something went wrong, make sure we know what we didn't get
                    bad_urls.append(url)

        return bad_urls, good_files


    def _parse_slack_mentions(self, text: str, parse_type: Literal['users', 'channels']) -> list[str | None]:
        """
        Parse out slack syntax in user messages and /slash commands in prep for LLM usage.

        ONLY parse's for `users` OR `channes` not both. If you want both run it 2 times.


        For Standar Messages:
            - <@USER_ID> and <#CHANNEL_ID|>
                - EX: <@U09S4H26G> for `@John Doe`
                - EX: <#C0957BD49H6|> for # all-hands

        For /slash Commands:
            - <@USER_ID|display_name> and <#CHANNEL_ID|channel_name>
                - EX: <@U09S4H26G|johndoe> for `@John Doe`
                - EX: <#C0957BD49H6|all-hands> for # all-hands


        The non-standardization will probably drive you insane, but....
        """
        if parse_type == 'users':
            matches = set(re.findall(r'<@([A-Z0-9]+)(?:\|[^>]*)?>', text))
        elif parse_type == 'channels':
            matches = set(re.findall(r'<#([A-Z0-9]+)(?:\|[^>]*)?>', text))
        return list(matches) or []


    def _map_slack_encodings_to_readable_text(self, info: dict, mentions: list[str] | None, slack_type: Literal['users', 'channels']) -> dict:
        names_map = {}
        for id in mentions:
            if name := info.get(id, {}).get('name'):
                if slack_type == 'users':
                    names_map[f'<@{id}>'] = name # user
                elif slack_type == 'channels':
                    names_map[f'<#{id}|>'] = f'# {name}' # channel
        return names_map


    def _replace_multiple_substrings(self, text: str, replacements: dict[str, str]) -> str:
        result = text
        for old, new in replacements.items():
            result = result.replace(old, new)
        return result


    @async_cached(cache=TTLCache(maxsize=1, ttl=600))
    async def _query_slack_for_user_ids(self, client: AsyncWebClient, logger: Logger) -> dict[str, Any] | dict[None, None]:

        users_response = await client.users_list(include_locale=True)
        users = users_response.data['members']
        logger.info(f'\n{"*"*200}\nusers: {len(users)}\n{"*"*200}')

        users_dict = {}
        for user in users:
            if user['id'] != 'USLACKBOT' and not user['is_bot'] and not user['deleted']:

                filtered_user = {}
                user_profile = user['profile']
                if (f := user_profile.get('first_name')) and (l := user_profile.get('last_name')):
                    filtered_user['name'] = f'{f} {l}'
                else:
                    filtered_user['name'] = user_profile.get('real_name')
                filtered_user['id'] = user['id']
                filtered_user['team_id'] = user['team_id']
                filtered_user['locale'] = user['locale']
                filtered_user['user_time_zone_info'] = {
                    'tz': user['tz'],
                    'tz_lable': user['tz_label']
                }
                users_dict[user['id']] = filtered_user
        return users_dict


    @async_cached(cache=TTLCache(maxsize=1, ttl=600))
    async def _query_slack_for_channel_ids(self, client: AsyncWebClient, logger: Logger) -> dict[str, Any] | dict[None, None]:

        channels_response = await client.conversations_list(
            team_id='T0957BCU8C8',
            exclude_archived=True,
            types='public_channel'
        )
        channels = channels_response.data['channels']
        logger.info(f'\n{"*"*200}\nchannels: {len(channels)}\n{"*"*200}')

        # mpim = client.conversations_list(
        #     team_id='T0957BCU8C8',
        #     exclude_archived=True, types='mpim'
        # ).data['channels'] # type: ignore

        # im = client.conversations_list(
        #     team_id='T0957BCU8C8',
        #     exclude_archived=True, types='im'
        # ).data['channels'] # type: ignore

        active_channels = {}
        for channel in channels:
            if not channel['is_archived']:
                filtered_channel = {
                    'id': channel['id'],
                    'name': channel['name'],
                    'team_id': channel.get('context_team_id'),
                    'num_members': channel['num_members'],
                    'description': channel['purpose']['value']
                }
                active_channels[channel['id']] = filtered_channel
        return active_channels

