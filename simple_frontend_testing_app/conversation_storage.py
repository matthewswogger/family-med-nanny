import logfire
from pydantic_ai.messages import ModelMessage


class Database:
    def __init__(self):
        self.chat_history: list[ModelMessage] = []

    def get_messages(self) -> list[ModelMessage]:
        return self.chat_history

    def add_messages(self, messages: ModelMessage) -> None:
        self.chat_history.append(messages)
