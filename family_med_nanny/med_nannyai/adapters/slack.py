from pydantic_ai import Agent, BinaryContent
import logfire
import logging
from typing import Any

from med_nannyai.medication_journal import MedNannyAIUserID, MedicationJournals
from med_nannyai.core_ai import med_nanny_ai_agent, SessionDependencies

logger = logging.getLogger(__name__)

logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)


# from typing import reveal_type
# print(reveal_type(agent))


class MedNannyAI:
    def __init__(self, agent: Agent[SessionDependencies, str]):
        self._agent = agent
        self._message_history = []
        self._journal = MedicationJournals()

    async def process_user_input(
            self,
            user_message: str,
            user_name: str,
            user_id: int,
            image_files: list[tuple[str, str, Any]] | None = None,
            family_names_map: dict[str, str] | None = None
        ) -> str:

        family_users = [MedNannyAIUserID(id=id, name=name) for id, name in family_names_map.items()]

        # Prepare input content
        input_content = [user_message]

        # Add image files if provided
        if image_files:
            for url, content_type, content in image_files:
                if content_type.startswith('image/'):
                    input_content.append(BinaryContent(data=content, media_type=content_type))

        print('\n--------------------------------\n', flush=True)
        print(f'JOURNAL: {self._journal}', flush=True)
        print('\n--------------------------------\n', flush=True)

        deps = SessionDependencies(
            user_id=MedNannyAIUserID(id=user_id, name=user_name),
            family_users=family_users,
            journal=self._journal
        )

        agent_response = await self._agent.run(
            user_prompt=input_content,
            deps=deps,
            message_history=self._message_history
        )
        self._message_history = agent_response.all_messages()
        # self._message_history = agent_response.new_messages()

        return agent_response.output


Slack_MedNannyAI = MedNannyAI(
    agent=med_nanny_ai_agent,
)
