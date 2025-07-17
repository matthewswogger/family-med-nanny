from pathlib import Path
# from typing_extensions import TypedDict
from typing import Literal, TypedDict
from fastapi import Request
from pydantic_ai.exceptions import UnexpectedModelBehavior
from pydantic_ai.messages import (
    ModelMessage,
    ModelRequest,
    ModelResponse,
    TextPart,
    UserPromptPart,
)

from conversation_storage import Database


THIS_DIR = Path(__file__).parent


class ChatMessage(TypedDict):
    """
    Format of messages sent to the browser.
    """
    role: Literal['user', 'model']
    timestamp: str
    content: str


async def get_db(request: Request) -> Database:
    return request.state.db


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
