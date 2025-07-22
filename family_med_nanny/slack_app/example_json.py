
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


# slack_MedNannyAI:handle_message_events
this_is_the_message_sent_when_image_is_uploaded = {
    'text': "I'm uploading a photo",
    'files': [
        {
            'id': 'F097BBZM9FS',
            'created': 1753065368,
            'timestamp': 1753065368,
            'name': 'Screenshot 2025-07-18 at 7.25.33\u202fPM.png',
            'title': 'Screenshot 2025-07-18 at 7.25.33\u202fPM.png',
            'mimetype': 'image/png',
            'filetype': 'png',
            'pretty_type': 'PNG',
            'user': 'U0957BCUP7S',
            'user_team': 'T0957BCU8C8',
            'editable': False,
            'size': 387519,
            'mode': 'hosted',
            'is_external': False,
            'external_type': '',
            'is_public': True,
            'public_url_shared': False,
            'display_as_bot': False,
            'username': '',
            'url_private': 'https://files.slack.com/files-pri/T0957BCU8C8-F097BBZM9FS/screenshot_2025-07-18_at_7.25.33___pm.png',
            'url_private_download': 'https://files.slack.com/files-pri/T0957BCU8C8-F097BBZM9FS/download/screenshot_2025-07-18_at_7.25.33___pm.png',
            'media_display_type': 'unknown',
            'thumb_64': 'https://files.slack.com/files-tmb/T0957BCU8C8-F097BBZM9FS-562e025ddc/screenshot_2025-07-18_at_7.25.33___pm_64.png',
            'thumb_80': 'https://files.slack.com/files-tmb/T0957BCU8C8-F097BBZM9FS-562e025ddc/screenshot_2025-07-18_at_7.25.33___pm_80.png',
            'thumb_160': 'https://files.slack.com/files-tmb/T0957BCU8C8-F097BBZM9FS-562e025ddc/screenshot_2025-07-18_at_7.25.33___pm_160.png',
            'thumb_360': 'https://files.slack.com/files-tmb/T0957BCU8C8-F097BBZM9FS-562e025ddc/screenshot_2025-07-18_at_7.25.33___pm_360.png',
            'thumb_360_w': 304,
            'thumb_360_h': 360,
            'thumb_480': 'https://files.slack.com/files-tmb/T0957BCU8C8-F097BBZM9FS-562e025ddc/screenshot_2025-07-18_at_7.25.33___pm_480.png',
            'thumb_480_w': 405,
            'thumb_480_h': 480,
            'thumb_720': 'https://files.slack.com/files-tmb/T0957BCU8C8-F097BBZM9FS-562e025ddc/screenshot_2025-07-18_at_7.25.33___pm_720.png',
            'thumb_720_w': 607,
            'thumb_720_h': 720,
            'thumb_800': 'https://files.slack.com/files-tmb/T0957BCU8C8-F097BBZM9FS-562e025ddc/screenshot_2025-07-18_at_7.25.33___pm_800.png',
            'thumb_800_w': 800,
            'thumb_800_h': 948,
            'thumb_960': 'https://files.slack.com/files-tmb/T0957BCU8C8-F097BBZM9FS-562e025ddc/screenshot_2025-07-18_at_7.25.33___pm_960.png',
            'thumb_960_w': 810,
            'thumb_960_h': 960,
            'thumb_1024': 'https://files.slack.com/files-tmb/T0957BCU8C8-F097BBZM9FS-562e025ddc/screenshot_2025-07-18_at_7.25.33___pm_1024.png',
            'thumb_1024_w': 864,
            'thumb_1024_h': 1024,
            'original_w': 1574,
            'original_h': 1866,
            'thumb_tiny': 'AwAwACmoJDk8Lz7CnNIwHIj/AAAqGnbm27dxx6ZoAXf7Cjf7Cm5OMZ49KKAHb/YflRvPoPyplFACilGTSCnKGwCOATjOcUwDa2QByT0xzSZp4WUKoXOGOVA9R3oBl4xv4BI68DuaAIzSU4sSoUngdBTaQC/Sj8M0CnKhYEgjjr7UANxxQfpinbOnzLz70YyeD+fFADaSlNJQB//Z',
            'permalink': 'https://dayofmay.slack.com/files/U0957BCUP7S/F097BBZM9FS/screenshot_2025-07-18_at_7.25.33___pm.png',
            'permalink_public': 'https://slack-files.com/T0957BCU8C8-F097BBZM9FS-ebe3ae838a',
            'skipped_shares': True,
            'has_rich_preview': False,
            'file_access': 'visible'
        }
    ],
    'upload': False,
    'user': 'U0957BCUP7S',
    'display_as_bot': False,
    'blocks': [
        {
            'type': 'rich_text',
            'block_id': 'WSAW0',
            'elements': [
                {
                    'type': 'rich_text_section',
                    'elements': [
                        {
                            'type': 'text',
                            'text': "I'm uploading a photo"
                        }
                    ]
                }
            ]
        }
    ],
    'type': 'message',
    'ts': '1753065376.418809',
    'client_msg_id': '668b9b2e-a95e-4712-8077-2a9cbbe665aa',
    'channel': 'C0957BD49H6',
    'subtype': 'file_share',
    'event_ts': '1753065376.418809',
    'channel_type': 'channel'
}

################################################################################

body = {
    'token': 'MucpYvMabH7XHWcpgZtxLr0l',
    'team_id': 'T0957BCU8C8',
    'context_team_id': 'T0957BCU8C8',
    'context_enterprise_id': None,
    'api_app_id': 'A09630R5CKA',
    'event': {
        'type': 'file_shared',
        'file_id': 'F096QN4UZFE',
        'user_id': 'U0957BCUP7S',
        'file': {
            'id': 'F096QN4UZFE'
        },
        'channel_id': 'C0957BD49H6',
        'event_ts': '1753081140.000800'
    },
    'type': 'event_callback',
    'event_id': 'Ev096MGWDFK7',
    'event_time': 1753081140,
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
    'event_context': '4-eyJldCI6ImZpbGVfc2hhcmVkIiwidGlkIjoiVDA5NTdCQ1U4QzgiLCJhaWQiOiJBMDk2MzBSNUNLQSIsImNpZCI6IkMwOTU3QkQ0OUg2In0'
}


event = {
    'type': 'file_shared',
    'file_id': 'F096QN4UZFE',
    'user_id': 'U0957BCUP7S',
    'file': {
        'id': 'F096QN4UZFE'
    },
    'channel_id': 'C0957BD49H6',
    'event_ts': '1753081140.000800'
}

