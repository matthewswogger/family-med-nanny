from fastapi import FastAPI, Request
from urllib.parse import parse_qsl
import json

from slack_app.main import SLACK_HANDLER


def parse_req_body(bytes_data):
    decoded = bytes_data.decode('utf-8').strip()

    if decoded.startswith('{') or decoded.startswith('['):
        return json.loads(decoded)

    return {k: v for k, v in parse_qsl(decoded)}



app = FastAPI()

@app.get('/')
async def root():
    return {'message': 'Hello World'}


@app.post('/slack/events')
async def slack_events(req: Request):

    print('-'*100, flush=True)
    print(f'\nmethod:\n {req.method}', flush=True)
    print(f'\nurl:\n {req.url}', flush=True)
    print(f'\nheaders:\n {req.headers}', flush=True)
    print(f'\nquery_params:\n {req.query_params}', flush=True)
    print(f'\npath_params:\n {req.path_params}', flush=True)
    print(f'\nclient:\n {req.client}', flush=True)
    print(f'\ncookies:\n {req.cookies}', flush=True)

    bod = await req.body()
    print(f'\nbody():\n {parse_req_body(bod)}', flush=True)

    # print(f'\njson():\n {await req.json()}', flush=True)
    # print(f'\napp:\n {req.app}', flush=True)
    # print(f'\nstate:\n {req.state}', flush=True)
    print('-'*100, flush=True)

    # print(f'\n\n/fastapi req:\n {req}\n\n', flush=True)
    return await SLACK_HANDLER.handle(req)


# /hey - my response
_ = {
    'token': 'MucpYvMabH7XHWcpgZtxLr0l',
    'team_id': 'T0957BCU8C8',
    'context_team_id': 'T0957BCU8C8',
    'context_enterprise_id': None,
    'api_app_id': 'A09630R5CKA',
    'type': 'event_callback',
    'event_id': 'Ev095G62EDML',
    'event_time': 1752376272,
    'is_ext_shared_channel': False,
    'event_context': '4-eyJldCI6Im1lc3NhZ2UiLCJ0aWQiOiJUMDk1N0JDVThDOCIsImFpZCI6IkEwOTYzMFI1Q0tBIiwiY2lkIjoiQzA5NTdCRDQ5SDYifQ',
    'event': {
        'user': 'U0957BCUP7S',
        'type': 'message',
        'ts': '1752376272.687209',
        'client_msg_id': '8c809563-ae4a-4233-a091-d4abaee74bb6',
        'text': 'howdy <@U0957BCUP7S> yes <#C094D5GPBTM|> other',
        'team': 'T0957BCU8C8',
        'blocks': [
            {
                'type': 'rich_text',
                'block_id': 'pC6gQ',
                'elements': [
                    {
                        'type': 'rich_text_section',
                        'elements': [
                            {
                                'type': 'text',
                                'text': 'howdy '
                            },
                            {
                                'type': 'user',
                                'user_id': 'U0957BCUP7S'
                            },
                            {
                                'type': 'text',
                                'text': ' yes '
                            },
                            {
                                'type': 'channel',
                                'channel_id': 'C094D5GPBTM'
                            },
                            {
                                'type': 'text',
                                'text': ' other'
                            }
                        ]
                    }
                ]
            }
        ],
        'channel': 'C0957BD49H6',
        'event_ts': '1752376272.687209',
        'channel_type': 'channel'
    },
    'authorizations': [
        {
            'enterprise_id': None,
            'team_id': 'T0957BCU8C8',
            'user_id': 'U0959PTD7KM',
            'is_bot': True,
            'is_enterprise_install': False
        }
    ],
}
