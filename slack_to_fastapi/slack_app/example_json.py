
# what comes through the fastapi app
req = {
    'token': 'MucpYvMabH7XHWcpgZtxLr0l',
    'team_id': 'T0957BCU8C8',
    'context_team_id': 'T0957BCU8C8',
    'context_enterprise_id': None,
    'api_app_id': 'A09630R5CKA',
    'event': {
        'user': 'U0957BCUP7S',
        'type': 'message',
        'ts': '1752906033.277199',
        'client_msg_id': '4d4d3a7d-37d7-44be-bd73-7cf0b0502de3',
        'text': 'hello',
        'team': 'T0957BCU8C8',
        'blocks': [
            {
                'type': 'rich_text',
                'block_id': 'ZL1yL',
                'elements': [
                    {
                        'type': 'rich_text_section',
                        'elements': [
                            {
                                'type': 'text',
                                'text': 'hello'
                            }
                        ]
                    }
                ]
            }
        ],
        'channel': 'C0957BD49H6',
        'event_ts': '1752906033.277199',
        'channel_type': 'channel'
    },
    'type': 'event_callback',
    'event_id': 'Ev096K0YEDPC',
    'event_time': 1752906033,
    'authorizations': [
        {
            'enterprise_id': None,
            'team_id': 'T0957BCU8C8',
            'user_id': 'U0959PTD7KM',
            'is_bot': True,
            'is_enterprise_install': False
        }
    ],
    'is_ext_shared_channel': False,
    'event_context': '4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDk1N0JDVThDOCIsImFpZCI6IkEwOTYzMFI1Q0tBIiwiY2lkIjoiQzA5NTdCRDQ5SDYifQ'
}


# users_and_channels_info = GetSlackUserAndChannelInfo()
# users_info, channels_info = users_and_channels_info(client)

users_info = [
    {
        'user_name': 'Matthew May',
        'user_id': 'U0957BCUP7S',
        'slack_team_id': 'T0957BCU8C8',
        'locale': 'en-US',
        'user_time_zone_info': {
            'tz': 'America/New_York',
            'tz_lable': 'Eastern Daylight Time'
        }
    },
    # ... more users (excluding bots, USLACKBOT, and deleted users)
]

channels_info = [
    {
        'id': 'C094D5GPBTM',
        'name': 'new-channel',
        'team_id': 'T0957BCU8C8',
        'num_members': 1,
        'description': 'This channel is for everything #new-channel. Hold meetings, share docs, and make decisions together with your team.'
    },
    {
        'id': 'C0957BD49H6',
        'name': 'all-day-of-may',
        'team_id': 'T0957BCU8C8',
        'num_members': 3,
        'description': 'Share announcements and updates about company news, upcoming events, or teammates who deserve some kudos. ⭐'
    },
    {
        'id': 'C0957BD4UFJ',
        'name': 'social',
        'team_id': 'T0957BCU8C8',
        'num_members': 1,
        'description': 'Other channels are for work. This one’s just for fun. Get to know your teammates and show your lighter side. 🎈'
    },
    # ... more channels (excluding archived ones)
]

#########################################################


event_message_example = {
    'user': 'U0957BCUP7S',
    'type': 'message',
    'ts': '1752895926.043579',
    'client_msg_id': '57081ede-2fbc-453d-82d8-a12b2ed87b21',
    'text': 'hello <@U0957BCUP7S> and this here <#C0957BD4UFJ|> yes sir',
    'team': 'T0957BCU8C8',
    'blocks': [
        {
            'type': 'rich_text',
            'block_id': 'N/u9r',
            'elements': [
                {
                    'type': 'rich_text_section',
                    'elements': [
                        {
                            'type': 'text',
                            'text': 'hello '
                        },
                        {
                            'type': 'user',
                            'user_id': 'U0957BCUP7S'
                        },
                        {
                            'type': 'text',
                            'text': ' and this here '
                        },
                        {
                            'type': 'channel',
                            'channel_id': 'C0957BD4UFJ'
                        },
                        {
                            'type': 'text',
                            'text': ' yes sir'
                        }
                    ]
                }
            ]
        }
    ],
    'channel': 'C0957BD49H6',
    'event_ts': '1752895926.043579',
    'channel_type': 'channel'
}

command_hey_example = {
    'token': 'MucpYvMabH7XHWcpgZtxLr0l',
    'team_id': 'T0957BCU8C8',
    'team_domain': 'dayofmay',
    'channel_id': 'C0957BD49H6',
    'channel_name': 'all-day-of-may',
    'user_id': 'U0957BCUP7S',
    'user_name': 'matthewswogger',
    'command': '/hey',
    'text': 'and this channel <#C0957BD49H6|all-day-of-may> and this user <@U0957BCUP7S|matthewswogger> for sure',
    'api_app_id': 'A09630R5CKA',
    'is_enterprise_install': 'false',
    'response_url': 'https://hooks.slack.com/commands/T0957BCU8C8/9245712913776/3WKHD0MFuXzce3MZfZdLn7QA',
    'trigger_id': '9245712914320.9177386960416.4efb39a5fe50cf2e0a69d8efd6ca367a'
}
