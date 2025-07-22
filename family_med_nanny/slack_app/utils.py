import httpx
import os
import base64
from typing import Any
import asyncio
from slack_sdk import WebClient
from typing import Any, Literal
import functools


class SlackHandler:
    def __init__(self):
        self.after_pad: str = f'{"*"*20}'
        # self.before_pad: str = f'\n{"*"*20}\n'
        self.before_pad: str = f'\n{self.after_pad}\n'

    def handle_commands(self, args):
        # acknowledge using mysterious slack magic
        args.ack()
        # ack(f"Hi <@{command['user_id']}>!")

        args.logger.info(
            f'{self.before_pad}'
            f'Command:\n{args.command}\n'
            f'{self.after_pad}'
        )

        # 1) get the things you need from `command`, `context`
        channel_id = args.command.get('channel_id')
        user_text = args.command.get('text')
        # user_mentions, channel_mentions = parse_slack_mentions(user_text)


        # 2) use `MedNannyAI` to craft what will be said to the user etc


        # 3) send whatever message you need to to the user
        response = args.client.chat_postMessage(
            channel=channel_id,
            text=f'Here is what I got for you: {user_text}',
        )

    def handle_messages(self, args):
        args.logger.info(
            f'{self.before_pad}'
            f'Message:\n{args.message}\n'
            f'Event:\n{args.event}\n'
            f'{self.after_pad}'
        )

        # enriched_user_ids = EnrichUserIDs(users_info, request_type='message')
        # enriched_channel_ids = EnrichChannelIDs(channels_info, request_type='message')


        urls = self._look_for_possible_files_being_uploaded(args.message, strict=False)

        args.logger.info(
            f'{self.before_pad}'
            f'File urls:\n{urls}\n'
            f'{self.after_pad}'
        )

        bad_urls, good_files = asyncio.run(self._run_get_files_from_slack_async(urls))

        args.logger.info(
            f'{self.before_pad}'
            f'Bad urls:\n{len(bad_urls)}\n'
            f'Good files:\n{len(good_files)}\n'
            f'{self.after_pad}'
        )

        user_text = args.message.get('text')
        channel_id = args.message.get('channel')


        # user_text = event.get('text')
        # channel_id = event.get('channel')
        # user_id = event.get('user')
        # event_ts = event.get('event_ts') or event.get('ts')

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

        response = args.client.chat_postMessage(
            channel=channel_id,
            # text=med_nanny_response
            text=f'Here is what I got for you: {user_text}',
        )
        # response = args.client.chat_postEphemeral(
        #     channel=channel_id,
        #     user=user_id,
        #     text=med_nanny_response
        # )

    def handle_events(self, args):
        args.logger.info(
            f'{self.before_pad}'
            f'Event:\n{args.event}\n'
            f'{self.after_pad}'
        )

        if args.event.get('type') in ['reaction_added']:

            channel_id = args.event.get('item').get('channel')
            user_reaction = args.event.get('reaction')

            response = args.client.chat_postMessage(
                channel=channel_id,
                # text=med_nanny_response
                text=f'Here is what I got for you: {user_reaction}',
            )
            # response = args.client.chat_postEphemeral(
            #     channel=channel_id,
            #     user=user_id,
            #     text=med_nanny_response
            # )

    def _look_for_possible_files_being_uploaded(self,message, strict: bool=False) -> list[str | None]:
        '''
        If a message has a 'files' block in it,
            we take a look for 'mimetype' of 'image/*' so we can get the urls for them.
            - This allows the bot to know that someone uploaded
                a pic of a prescription bottle and it might need to OCR that bad boy.

        If strict is False, we will return all the urls, not just the image urls.
        '''
        file_blocks = message.get('files', [])
        urls = []

        if strict:
            urls = [file.get('url_private') for file in file_blocks if file.get('mimetype', '').startswith('image/')]
        else:
            urls = [file.get('url_private') for file in file_blocks if file.get('mimetype')]
        return urls

    async def _get_files_from_slack_async(self, urls: list[str | None]) -> tuple[list[str | None], list[tuple[str, str, Any] | None]]:
        '''
        Async version: Get files from Slack.
        - If the file is an image, we get the base64 encoded version of it.
        - If the file is not an image, we get the raw content of the file.
        - If something goes wrong, we add the url to the bad_urls list.
        '''
        SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
        headers = {'Authorization': f'Bearer {SLACK_BOT_TOKEN}'}

        bad_urls:   list[str | None] = []
        good_files: list[tuple[str, str, Any] | None] = []

        async with httpx.AsyncClient() as client:
            for url in urls:
                response = await client.get(url=url, headers=headers)
                if response.is_success:
                    if response.headers['content-type'].startswith('image/'):
                        b64_encoded = base64.b64encode(response.content).decode('utf-8')
                        good_files.append((url, response.headers['content-type'], b64_encoded))

                    else: # files, but not images, save for later I guess
                        good_files.append((url, response.headers['content-type'], response.content))

                else: # something went wrong, make sure we know what we didn't get
                    bad_urls.append(url)

        return bad_urls, good_files


    async def _run_get_files_from_slack_async(self, url_list: list[str]) -> tuple[list[str | None], list[tuple[str, str, Any] | None]]:
        bad_urls, good_files = await self._get_files_from_slack_async(url_list)
        return bad_urls, good_files









###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################
###############################################################################

@functools.cache
class GetSlackUserAndChannelInfo:
    def __init__(
            self,
            client: WebClient
        ) -> tuple[list[dict[str, Any] | None], list[dict[str, Any] | None]]:

        print('I guess it has not been called yet', flush=True)
        self.users = self._query_slack_for_user_ids(client)
        self.channels = self._query_slack_for_channel_ids(client)

    def get_it_all(self):
        return self.users, self.channels

    # def __call__(
    #         self,
    #         client: WebClient
    #     ) -> tuple[list[dict[str, Any] | None], list[dict[str, Any] | None]]:

    #     users = self._query_slack_for_user_ids(client)
    #     channels = self._query_slack_for_channel_ids(client)

    #     return users, channels

    def _query_slack_for_user_ids(self, client: WebClient) -> list[dict[str, Any] | None]:
        users = client.users_list(include_locale=True).data['members'] # type: ignore

        users_list = []
        for user in users:
            if user['id'] != 'USLACKBOT' and not user['is_bot'] and not user['deleted']:

                filtered_user = {}
                user_profile = user['profile']
                if (f := user_profile.get('first_name')) and (l := user_profile.get('last_name')):
                    filtered_user['user_name'] = f'{f} {l}'
                else:
                    filtered_user['user_name'] = user_profile.get('real_name')

                filtered_user['user_id'] = user['id']
                filtered_user['slack_team_id'] = user['team_id']
                filtered_user['locale'] = user['locale']
                filtered_user['user_time_zone_info'] = {
                    'tz': user['tz'],
                    'tz_lable': user['tz_label']
                }

                users_list.append(filtered_user)
        return users_list

    def _query_slack_for_channel_ids(self, client: WebClient) -> list[dict[str, Any] | None]:
        channels = client.conversations_list(
            team_id='T0957BCU8C8',
            exclude_archived=True,
            types='public_channel'
        ).data['channels'] # type: ignore

        # mpim = client.conversations_list(
        #     team_id='T0957BCU8C8',
        #     exclude_archived=True, types='mpim'
        # ).data['channels'] # type: ignore

        # im = client.conversations_list(
        #     team_id='T0957BCU8C8',
        #     exclude_archived=True, types='im'
        # ).data['channels'] # type: ignore

        active_channels = []
        for channel in channels:
            if not channel['is_archived']:
                filtered_channel = {
                    'id': channel['id'],
                    'name': channel['name'],
                    'team_id': channel.get('context_team_id'),
                    'num_members': channel['num_members'],
                    'description': channel['purpose']['value']
                }
                active_channels.append(filtered_channel)
        return active_channels


class EnrichUserIDs:
    def __init__(
            self,
            users_info: list[dict[str, Any] | None],
            request_type: Literal['message']
        ):
        self.request_type = request_type
        self.users_info = users_info

    def __call__(
            self,
            user_id: str,
            user_name: str,
            user_text_object: list[dict[str, str]] | str,
            client: WebClient
        ) -> str:
        self.user_id = user_id
        self.user_name = user_name

        if self.request_type == 'message' and isinstance(user_text_object, list):
            self.user_text_object = user_text_object
        else:
            pass

        return 'hi'


    def __str__(self) -> str:
        return f'<@{self.user_id}|{self.user_name}>'


class EnrichChannelIDs:
    def __init__(
            self,
            channels_info: list[dict[str, Any] | None],
            request_type: Literal['message']
        ):
        self.request_type = request_type
        self.channels_info = channels_info

    def __call__(self, text: str) -> str:
        return f'<#{self.channel_id}>'

    def __str__(self) -> str:
        return f'<#{self.channel_id}|{self.channel_name}>'



# def parse_slack_mentions(text: str) -> tuple[list[str | None], list[str | None]]:
#     # matches this:
#     #   <@USER_ID> or <@USER_ID|display_name>
#     user_matches = set(re.findall(r'<@([A-Z0-9]+)(?:\|[^>]*)?>', text))

#     # matches this:
#     #   <#CHANNEL_ID|> or <#CHANNEL_ID|channel_name>
#     channel_matches = set(re.findall(r'<#([A-Z0-9]+)(?:\|[^>]*)?>', text))

#     return list(user_matches) or [], list(channel_matches) or []


# def parse_slack_event(event: dict[str, Any]):
#     user_text: str = event.get('text', '')
#     channel_id: str | None = event.get('channel')
#     user_id: str | None = event.get('user')
#     event_ts: str | None = event.get('event_ts') or event.get('ts')
#     user_mentions, channel_mentions = parse_slack_mentions(user_text)








#     all_slack_user_ids = ['U0957BCUP7S']
#     user_name_map = lambda x: f'<@{x}>'
#     slack_user_names_map = {
#         user_name_map('U0957BCUP7S'): 'Matthew May',
#     }

    # # client.conversations_list : Lists all channels in a Slack team.
    #     # x = client.conversations_list(
    #     #     team_id='T0957BCU8C8',
    #     #     exclude_archived=True,
    #     #     types='public_channel,private_channel,mpim,im'
    #     # )
    #     # x.data['channels']
    # #  conversations.info  ,    conversations.members
    # all_slack_channel_ids = ['C0957BD4UFJ', 'C0957BD49H6']
    # channel_name_map = lambda x: f'<#{x}|>'

    # for i in all_slack_channel_ids:
    # slack_channel_names_map = {
    #     channel_name_map('C0957BD4UFJ'): '#social',
    #     channel_name_map('C0957BD49H6'): '#all-day-of-may'
    # }



#     return



# def replace_multiple_substrings(text: str, replacements: dict[str, str]) -> str:
#     result = text
#     for old, new in replacements.items():
#         result = result.replace(old, new)
#     return result



# def replacemy_func_multiple_substrings(
#         text: str,
#         endpoint_type: Literal['command_hey', 'event_message']
#     ) -> str:
#     if endpoint_type == 'command_hey':
#         pass
#     elif endpoint_type == 'event_message':
#         user_name_map = lambda x: f'<@{x}>'
#         channel_name_map = lambda x: f'<#{x}|>'

#         slack_user_names_map = {
#             user_name_map('U0957BCUP7S'): 'Matthew May',
#         }
#         slack_channel_names_map = {
#             channel_name_map('C0957BD4UFJ'): '#social',
#             channel_name_map('C0957BD49H6'): '#all-day-of-may'
#         }

#     llm_user_text = replace_multiple_substrings(text, slack_user_names_map)
#     llm_user_text = replace_multiple_substrings(llm_user_text, slack_channel_names_map)

#     return llm_user_text





