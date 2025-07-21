from slack_sdk import WebClient
from typing import Any, Literal


class GetSlackUserAndChannelInfo:
    def __call__(
            self,
            client: WebClient
        ) -> tuple[list[dict[str, Any] | None], list[dict[str, Any] | None]]:

        users = self._query_slack_for_user_ids(client)
        channels = self._query_slack_for_channel_ids(client)

        return users, channels

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
        # self.channels_info = channels_info

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





