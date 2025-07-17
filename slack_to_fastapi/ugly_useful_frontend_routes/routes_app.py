import json
from datetime import datetime, timezone
from typing import Annotated, Literal, TypedDict
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import Response, StreamingResponse
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    TextPart,
    UserPromptPart,
)

from med_nannyai import (
    # MedNannyAI,
    agent,
    SessionDependencies,
    SlackUserIdentification,
    MedicationJournal
)



class Database:
    def __init__(self):
        self.chat_history: list[ModelMessage] = []

    def get_messages(self) -> list[ModelMessage]:
        return self.chat_history

    def add_messages(self, messages: ModelMessage) -> None:
        self.chat_history.append(messages)


async def get_db(request: Request) -> Database:
    try:
        return request.state.db
    except AttributeError:
        return Database()



class ChatMessage(TypedDict):
    """
    Format of messages sent to the browser.
    """
    role: Literal['user', 'model']
    timestamp: str
    content: str

def to_chat_message(m: ModelMessage) -> ChatMessage:
    first_part = m.parts[0]
    if isinstance(m, ModelRequest):
        if isinstance(first_part, UserPromptPart):
            assert isinstance(first_part.content, str)
            return ChatMessage(
                role='user',
                timestamp=first_part.timestamp.isoformat(),
                content=first_part.content,
            )
    elif isinstance(m, ModelResponse):
        if isinstance(first_part, TextPart):
            return ChatMessage(
                role='model',
                timestamp=m.timestamp.isoformat(),
                content=first_part.content,
            )
    raise UnexpectedModelBehavior(f'Unexpected message type for chat app: {m}')




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

    deps = SessionDependencies(
        user_info=SlackUserIdentification(user_id=123, user_name='John Doe'),
        medication_journal=MedicationJournal()
    )

    async with agent.run_stream(user_prompt, deps=deps, message_history=database.get_messages()) as result:
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
