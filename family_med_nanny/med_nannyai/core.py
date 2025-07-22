from datetime import date#, datetime
from dataclasses import dataclass
from pydantic import Field
from pydantic_ai import Agent, RunContext, ImageUrl, Tool
import logfire

from .medication_journal import MedicationJournal, MedicationJournalEntry
from .prescription_extraction import read_label_medication_bottle


logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)


########################################################################
# Data Models
########################################################################

@dataclass
class SlackUserIdentification:
    user_id: int = Field(description="The user's id")
    user_name: str = Field(description="The user's name")

@dataclass
class SessionDependencies:
    medication_journal: MedicationJournal
    user_info: SlackUserIdentification = Field(
        description='The user\'s information'
    )
    todays_date: date = date.today()

########################################################################
# Tools
########################################################################

async def medication_journal_add_entry(
        ctx: RunContext[SessionDependencies],
        medication_name: str,
        medication_frequency: str,
        medication_start_date: date,
        medication_end_date: date | None,
        medication_notes: str | None
    ) -> MedicationJournalEntry | None:
    """
    Add a medication journal entry to the user's medication journal
    """
    entry = MedicationJournalEntry(
        medication_name=medication_name,
        medication_frequency=medication_frequency,
        medication_start_date=medication_start_date,
        medication_end_date=medication_end_date,
        medication_notes=medication_notes
    )
    ctx.deps.medication_journal.add_entry(ctx.deps.user_info.user_id, entry)
    return entry


async def medication_journal_get_entry(
        ctx: RunContext[SessionDependencies],
        index: int
    ) -> MedicationJournalEntry | None:
    """
    Get a specific medication journal entry by index for the current user
    """
    return ctx.deps.medication_journal.get_entry(ctx.deps.user_info.user_id, index)


async def medication_journal_get_all_entries(
        ctx: RunContext[SessionDependencies]
    ) -> list[MedicationJournalEntry]:
    """
    Get all medication journal entries for the current user
    """
    return ctx.deps.medication_journal.get_entries(ctx.deps.user_info.user_id)


async def image_read_label_medication_bottle() -> ImageUrl:
    """
    Read the label on a medication bottle and return the text
    """
    return await read_label_medication_bottle()


tools = [
    Tool(medication_journal_add_entry, takes_ctx=True),
    Tool(medication_journal_get_entry, takes_ctx=True),
    Tool(medication_journal_get_all_entries, takes_ctx=True),
    Tool(image_read_label_medication_bottle, takes_ctx=False),
]

########################################################################
# Instructions
########################################################################

medication_assistant_general_instructions = """\
You're an assistant to help a family manage their medications.
This means that at least one of the family members has a very complex medication regimen.
This also usually means that the other family members are acting as
caregivers for the person with the complex medication regimen.
While all family members may take some medications, you will mostly be handling the medications
for the person with the complex medication regimen.
Questions/messages you will most likely handle are:
- Have I taken my morning medications yet today?
- How many more days until I need to get a refill for medication `medication name`?
- Do I have any refills left for `medication name` or do I need to call it in?
- What's the dosage for `medication name` again?
- Just took my morning meds, give me a reminder when it's time to take my evening meds.
- Give me a reminder on Thursday to call in my medication.
"""

async def initialization_instructions(ctx: RunContext[SessionDependencies]) -> str:
    return (
        f"{medication_assistant_general_instructions}"
        f"\nThe current date is {ctx.deps.todays_date!r}"
        f"\nThe user's name is {ctx.deps.user_info.user_name!r}"
        f"\nThe user's id is {ctx.deps.user_info.user_id!r}"
    )

########################################################################
# Agent
########################################################################

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
    # from typing import reveal_type
    # print(reveal_type(agent))

########################################################################
# MedNannyAI
#   - is the class that is actually exposed to the rest
#     of the application
#   - The hope being that it can be generally useable
#     across all application integration options
########################################################################


class MedNannyAI:
    def __init__(self, agent: Agent[SessionDependencies, str]):
        self._agent = agent
        self._message_history = []

    def process_user_input(self, user_message: str, user_name: str, user_id: int) -> str:
        deps = SessionDependencies(
            user_info=SlackUserIdentification(user_id=user_id, user_name=user_name),
            medication_journal=MedicationJournal()
        )

        agent_response = self._agent.run_sync(
            user_prompt=user_message,
            deps=deps,
            message_history=self._message_history
        )
        self._message_history = agent_response.all_messages()
        # self._message_history = agent_response.new_messages()

        return agent_response.output

Slack_MedNannyAI = MedNannyAI(agent=med_nanny_ai_agent)

if __name__ == '__main__':
    # at top of file
    med_nanny = MedNannyAI(agent=med_nanny_ai_agent)

    # user message comes in

        # process user message to get out required info
        #   - user_id: we will always be told who the user is
        #           - slack id
        #           - phone number
        #           - etc
        #   - user_name: will always be able to get it, sometimes given it
        #           - slack often gives it
        #               - if not, the slack id will give us the ability to get it
        #           - phone number gives the ability to get it

    med_nanny_response = med_nanny.process_user_input('I need help.', 'Matthew May', 123)



