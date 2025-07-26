from pydantic_ai import Agent

from .instructions import initialization_instructions
from .data_models import SessionDependencies
from .tools import tools


med_nanny_ai_agent = Agent(
    model='openai:gpt-4.1-mini',
    instructions=initialization_instructions,
    deps_type=SessionDependencies,
    output_type=str,
    tools=tools,
    history_processors=[
        # TODO: add a history processor that will
        #   - store the messages in the database
        #   - store the messages in the slack channel
        #   - store the messages in the slack channel
    ]
)
