import asyncio
from datetime import datetime, date
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, Tool
import logfire

# from slack_to_fastapi.med_nannyai import medication_journal

logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)


class MedNannyAI:
    def __init__(self):
        pass

    def craft_message(self, event, context):
        pass

    def send_message(self, message, channel_id):
        pass

########################################################################
# Data Models
########################################################################

@dataclass
class MedicationJournalEntry:
    medication_name: str = Field(description='The name of the medication')
    medication_frequency: str = Field(description='The frequency of the medication')
    medication_start_date: str = Field(description='The start date of the medication')
    medication_end_date: str | None = Field(default=None, description='The end date of the medication')
    medication_notes: str | None = Field(default=None, description='Any notes about the medication')

class MedicationJournal:
    entries: dict[int, list[MedicationJournalEntry]] = {}

    @classmethod
    def add_entry(cls, user_id: int, entry: MedicationJournalEntry):
        if user_id not in cls.entries:
            cls.entries[user_id] = []
        cls.entries[user_id].append(entry)

    @classmethod
    def get_entry(cls, user_id: int, index: int) -> MedicationJournalEntry | None:
        if user_id not in cls.entries or index >= len(cls.entries[user_id]):
            return None
        return cls.entries[user_id][index]

    @classmethod
    def get_entries(cls, user_id: int) -> list[MedicationJournalEntry]:
        if user_id not in cls.entries:
            return []
        return cls.entries[user_id]


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
    todays_date: str = date.today().strftime('%Y-%m-%d')


########################################################################
# Agent
########################################################################

agent = Agent(
    model='openai:gpt-4.1-mini',
    # model='openai:gpt-4o',
    deps_type=SessionDependencies,
    output_type=str,
)

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

@agent.instructions
async def general_instructions() -> str:
    return medication_assistant_general_instructions


@agent.instructions
async def add_user_name(ctx: RunContext[SessionDependencies]) -> str:
    return f"The user's name is {ctx.deps.user_info.user_name!r}"

@agent.instructions
async def add_user_id(ctx: RunContext[SessionDependencies]) -> str:
    return f"The user's id is {ctx.deps.user_info.user_id!r}"

@agent.instructions
async def todays_date(ctx: RunContext[SessionDependencies]) -> str:
    return f"The current date is {ctx.deps.todays_date!r}"

########################################################################
# Tools
########################################################################

@agent.tool
async def add_medication_journal_entry(
        ctx: RunContext[SessionDependencies],
        medication_name: str,
        medication_frequency: str,
        medication_start_date: str,
        medication_end_date: str | None,
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
    # return entry
    return ctx.deps.medication_journal.get_entry(ctx.deps.user_info.user_id, -1)


@agent.tool
async def get_medication_journal_entry(
        ctx: RunContext[SessionDependencies],
        index: int
    ) -> MedicationJournalEntry | None:
    """
    Get a specific medication journal entry by index for the current user
    """
    return ctx.deps.medication_journal.get_entry(ctx.deps.user_info.user_id, index)


@agent.tool
async def get_all_medication_journal_entries(
        ctx: RunContext[SessionDependencies]
    ) -> list[MedicationJournalEntry]:
    """
    Get all medication journal entries for the current user
    """
    return ctx.deps.medication_journal.get_entries(ctx.deps.user_info.user_id)


########################################################################
# For use in CLI
########################################################################

async def main():
    deps = SessionDependencies(
        user_info=SlackUserIdentification(user_id=123, user_name='John Doe'),
        medication_journal=MedicationJournal()
    )
    await agent.to_cli(deps=deps)


if __name__ == '__main__':
    asyncio.run(main())
