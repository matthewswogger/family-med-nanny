import json
from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, Form
from fastapi.responses import Response, StreamingResponse
from pydantic_ai.messages import ModelResponse, TextPart

from conversation_storage import Database
from utils import get_db, to_chat_message
from ai import agent


async def stream_messages(user_prompt: str, database: Database):
    """
    Stream messages to the client.
        - First send the most recent user message.
        - Then stream the response from the agent.
        - Finally, add the response to the database.
    """
    yield json.dumps(
            {
                'role': 'user',
                'timestamp': datetime.now(tz=timezone.utc).isoformat(),
                'content': user_prompt
            }
        ).encode('utf-8') + b'\n'

    async with agent.run_stream(user_prompt, message_history=database.get_messages()) as result:
        async for text in result.stream(debounce_by=0.01):
            m_response = ModelResponse(parts=[TextPart(text)], timestamp=result.timestamp())
            yield json.dumps(to_chat_message(m_response)).encode('utf-8') + b'\n'

    database.add_messages(messages=m_response)


router = APIRouter()

DATABASE_DEPENDENCY = Annotated[Database, Depends(get_db)]

@router.get('/chat/')
async def get_chat_history_on_ui_loading(
        database: DATABASE_DEPENDENCY
    ) -> Response:

    msgs = database.get_messages()
    return Response(
        b'\n'.join(json.dumps(to_chat_message(m)).encode('utf-8') for m in msgs),
        media_type='text/plain',
    )


@router.post('/chat/')
async def post_chat(
        prompt: Annotated[str, Form()],
        database: DATABASE_DEPENDENCY
    ) -> StreamingResponse:

    return StreamingResponse(stream_messages(prompt, database), media_type='text/plain')
